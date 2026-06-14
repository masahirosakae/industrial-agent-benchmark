#!/usr/bin/env python3
"""Re-generate only the failed rows in an existing evaluation_set_v2 run.

Reads `<output-root>/<run-id>/answers.jsonl`, identifies rows where
`error` is non-empty or `answer_text` is empty, and regenerates only those
questions using the requested provider. Successful rows and their
`answers/<question_id>.txt` files are left untouched. After regeneration the
merged set is written back to `answers.jsonl` and `manifest.json` is refreshed
with retry metadata.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from eval_v2_common import (
    ANSWER_PROMPT_TEMPLATE_VERSION,
    DEFAULT_EVALUATION_SET,
    DEFAULT_OUTPUT_ROOT,
    check_prompt_leakage,
    get_provider,
    load_evaluation_questions,
    load_index_by_id,
    load_problem,
    read_jsonl,
    render_answer_prompt,
    safe_duration,
    utc_now_iso,
    write_jsonl,
)

SYSTEM_PROMPT = (
    "You are answering Industrial Agent Benchmark v1.1.0-pre tasks. "
    "Answer in Japanese. If the question requests JSON, return valid JSON only when possible."
)


def _row_is_failed(row: dict[str, Any]) -> bool:
    if row.get("error"):
        return True
    text = row.get("answer_text")
    if text is None:
        return True
    if isinstance(text, str) and not text.strip():
        return True
    return False


def _parse_question_id_filter(value: str | None) -> set[str] | None:
    if not value:
        return None
    ids = {part.strip() for part in value.split(",") if part.strip()}
    return ids or None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Retry only failed answers for an evaluation_set_v2 run."
    )
    parser.add_argument("--run-id", required=True, help="Run directory id under --output-root")
    parser.add_argument("--model-id", required=True, help="Neutral model id recorded in JSONL")
    parser.add_argument(
        "--provider",
        choices=["dummy", "fugu"],
        default="fugu",
        help="Model provider. dummy performs no network calls.",
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Root directory for evaluation outputs")
    parser.add_argument("--evaluation-set", default=str(DEFAULT_EVALUATION_SET), help="Path to evaluation_set_v2.yaml")
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Per-request timeout in seconds (overrides FUGU_TIMEOUT_SECONDS).",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=None,
        help="Max additional attempts after the first on transient errors (overrides FUGU_MAX_RETRIES).",
    )
    parser.add_argument(
        "--backoff-base-seconds",
        type=float,
        default=None,
        help="Base seconds for exponential backoff between retries (overrides FUGU_BACKOFF_BASE_SECONDS).",
    )
    parser.add_argument(
        "--question-ids",
        default=None,
        help="Optional comma-separated subset of question ids to retry. Must be among failed rows.",
    )
    parser.add_argument(
        "--include-success",
        action="store_true",
        help="Also re-run rows currently marked successful (rare; default off).",
    )
    args = parser.parse_args()

    output_root = Path(args.output_root)
    run_dir = output_root / args.run_id
    answers_dir = run_dir / "answers"
    answers_path = run_dir / "answers.jsonl"
    manifest_path = run_dir / "manifest.json"

    if not answers_path.exists():
        print(f"ERROR: {answers_path} not found. Run eval_v2_generate_answers.py first.", file=sys.stderr)
        return 2

    existing_rows = read_jsonl(answers_path)
    existing_by_qid = {str(row.get("question_id")): row for row in existing_rows}
    if len(existing_by_qid) != len(existing_rows):
        print("ERROR: duplicate question_id rows detected in answers.jsonl", file=sys.stderr)
        return 2

    questions = load_evaluation_questions(Path(args.evaluation_set))
    questions_by_id = {str(q["id"]): q for q in questions}
    index_by_id = load_index_by_id()

    # Determine the candidate set: failed rows (or all if --include-success).
    candidate_qids: list[str] = []
    for q in questions:
        qid = str(q["id"])
        row = existing_by_qid.get(qid)
        if row is None:
            candidate_qids.append(qid)
            continue
        if args.include_success or _row_is_failed(row):
            candidate_qids.append(qid)

    filter_ids = _parse_question_id_filter(args.question_ids)
    if filter_ids is not None:
        unknown = filter_ids - set(questions_by_id.keys())
        if unknown:
            print(f"ERROR: --question-ids contains unknown ids: {sorted(unknown)}", file=sys.stderr)
            return 2
        not_failed = [qid for qid in filter_ids if qid not in candidate_qids]
        if not_failed and not args.include_success:
            print(
                "ERROR: the following --question-ids are not currently failed (use --include-success to force):"
                f" {sorted(not_failed)}",
                file=sys.stderr,
            )
            return 2
        candidate_qids = [qid for qid in candidate_qids if qid in filter_ids]

    if not candidate_qids:
        print("No failed rows to retry. Nothing to do.")
        return 0

    print(f"Retry targets ({len(candidate_qids)}): {', '.join(candidate_qids)}")

    provider = get_provider(
        args.provider,
        args.model_id,
        timeout=args.timeout,
        max_retries=args.max_retries,
        backoff_base_seconds=args.backoff_base_seconds,
    )

    answers_dir.mkdir(parents=True, exist_ok=True)
    leakage_issues: dict[str, list[str]] = {}
    retried_results: dict[str, dict[str, Any]] = {}

    for qid in candidate_qids:
        q = questions_by_id[qid]
        problem = load_problem(qid, index_by_id)
        prompt = render_answer_prompt(q, problem)
        leaked_terms = check_prompt_leakage(prompt)
        if leaked_terms:
            leakage_issues[qid] = leaked_terms

        started = utc_now_iso()
        start_time = time.perf_counter()
        error = ""
        try:
            response = provider.generate(prompt, system_prompt=SYSTEM_PROMPT)
            answer_text = response.text.strip()
            provider_name = response.provider
            provider_model = response.model
        except Exception as exc:  # noqa: BLE001 - record per-row error
            answer_text = ""
            error = f"{type(exc).__name__}: {exc}"
            provider_name = args.provider
            provider_model = args.model_id
        end_time = time.perf_counter()
        finished = utc_now_iso()
        latency = safe_duration(start_time, end_time)

        # Only overwrite the per-question .txt when we have new content,
        # so a transient failure during retry does not blank out an earlier success.
        if answer_text or not (answers_dir / f"{qid}.txt").exists():
            (answers_dir / f"{qid}.txt").write_text(answer_text, encoding="utf-8", newline="\n")

        retried_results[qid] = {
            "run_id": args.run_id,
            "model_id": args.model_id,
            "provider": provider_name,
            "provider_model": provider_model,
            "question_id": qid,
            "answer_text": answer_text,
            "started_at": started,
            "finished_at": finished,
            "latency_seconds": latency,
            "temperature": 0,
            "prompt_template_version": ANSWER_PROMPT_TEMPLATE_VERSION,
            "error": error,
        }
        status = "OK" if not error and answer_text else f"FAIL({error or 'empty'})"
        print(f"  [{qid}] {status} ({latency:.2f}s)")

    # Rebuild answers.jsonl preserving evaluation_set order.
    merged_rows: list[dict[str, Any]] = []
    for q in questions:
        qid = str(q["id"])
        if qid in retried_results:
            merged_rows.append(retried_results[qid])
        elif qid in existing_by_qid:
            merged_rows.append(existing_by_qid[qid])
    # Preserve rows that exist only outside the current evaluation_set (defensive).
    seen = {str(r["question_id"]) for r in merged_rows}
    for row in existing_rows:
        if str(row.get("question_id")) not in seen:
            merged_rows.append(row)

    write_jsonl(answers_path, merged_rows)

    # Update manifest.json with retry info.
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {}
    manifest["run_id"] = args.run_id
    manifest["model_id"] = args.model_id
    manifest["provider"] = args.provider
    manifest["benchmark_version"] = manifest.get("benchmark_version", "v1.1.0-pre")
    manifest["evaluation_set"] = str(args.evaluation_set)
    manifest["question_count"] = len(merged_rows)
    manifest["temperature"] = 0
    manifest["prompt_template_version"] = ANSWER_PROMPT_TEMPLATE_VERSION
    manifest["prompt_leakage_count"] = manifest.get("prompt_leakage_count", 0) + sum(
        len(v) for v in leakage_issues.values()
    )
    manifest["dry_run"] = False
    retries_log = manifest.get("retries", [])
    retries_log.append(
        {
            "retried_at": utc_now_iso(),
            "target_question_ids": candidate_qids,
            "succeeded_question_ids": [
                qid for qid, r in retried_results.items() if not r["error"] and r["answer_text"]
            ],
            "failed_question_ids": [
                qid for qid, r in retried_results.items() if r["error"] or not r["answer_text"]
            ],
            "provider": args.provider,
            "timeout_seconds": args.timeout,
            "max_retries": args.max_retries,
            "backoff_base_seconds": args.backoff_base_seconds,
        }
    )
    manifest["retries"] = retries_log
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    # Final summary.
    new_failed = [qid for qid, r in retried_results.items() if r["error"] or not r["answer_text"]]
    print()
    print(f"answers.jsonl rows  : {len(merged_rows)} -> {answers_path}")
    print(f"Retried targets     : {len(candidate_qids)}")
    print(f"  succeeded         : {len(retried_results) - len(new_failed)}")
    print(f"  still failed      : {len(new_failed)}")
    if new_failed:
        for qid in new_failed:
            print(f"    - {qid}: {retried_results[qid]['error'] or 'empty answer'}")
    if leakage_issues:
        print("ERROR: prompt leakage detected:", file=sys.stderr)
        for qid, terms in leakage_issues.items():
            print(f"  - {qid}: {', '.join(terms)}", file=sys.stderr)
        return 1
    return 1 if new_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
