#!/usr/bin/env python3
"""Run Judge v2 for one evaluation run.

The script reuses scripts/prepare_judge_inputs_v2.py to materialize judge prompts.
It performs no network calls in --dry-run mode. By default, --judge-provider is
"dummy" and will not create benchmark judgements unless --write-dummy-judgements
is explicitly supplied.

Per-question failures (provider error, invalid JSON, etc.) are isolated:
the failing question is logged and skipped (no placeholder judgement file is
written), so it can be re-run later via --only-missing or --question-ids.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from eval_v2_common import (
    DEFAULT_EVALUATION_SET,
    DEFAULT_OUTPUT_ROOT,
    JUDGE_PROMPT_TEMPLATE_VERSION,
    extract_json_object,
    get_provider,
    load_evaluation_questions,
    normalize_judgement,
    safe_duration,
    utc_now_iso,
    write_jsonl,
)

SYSTEM_PROMPT = (
    "You are Judge v2 for Industrial Agent Benchmark v1.1.0-pre. "
    "Follow the provided scoring order exactly. Return parseable JSON only."
)


def load_manifest(run_dir: Path) -> dict[str, Any]:
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        return {}
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def prepare_judge_inputs(run_id: str, output_root: Path, evaluation_set: Path) -> None:
    script = Path(__file__).resolve().parent / "prepare_judge_inputs_v2.py"
    command = [
        sys.executable,
        str(script),
        run_id,
        "--results-root",
        str(output_root),
        "--evaluation-set",
        str(evaluation_set),
    ]
    subprocess.run(command, check=True)


def build_dummy_raw(model_id: str, q: dict[str, Any]) -> dict[str, Any]:
    return {
        "model_id": model_id,
        "question_id": q["id"],
        "layer": q.get("layer", ""),
        "category": q.get("category", ""),
        "difficulty": q.get("difficulty", 0),
        "domain": q.get("domain", ""),
        "final_score": 1,
        "must_have_missing_count": 0,
        "numeric_check_failed_ratio": 0.0,
        "generic_penalty_triggered": False,
        "critical_failure_triggered": False,
        "score_cap_applied": False,
        "structured_output_missing_count": 0,
        "judge_summary": "Dummy judgement; not a benchmark result.",
        "evidence_summary": "No model evidence evaluated in dummy mode.",
        "is_dummy_judgement": True,
    }


def _parse_question_id_filter(value):
    if not value:
        return None
    ids = {part.strip() for part in value.split(",") if part.strip()}
    return ids or None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Judge v2 over one run's judge_inputs.")
    parser.add_argument("--run-id", required=True, help="Run directory id under --output-root")
    parser.add_argument(
        "--model-id",
        default=None,
        help="Evaluated model id (recorded in judgements). Defaults to manifest model_id or run_id.",
    )
    parser.add_argument(
        "--judge-model",
        default=None,
        help="Judge model id passed to the provider (independent of --model-id). Defaults to env FUGU_JUDGE_MODEL, then env FUGU_MODEL, then --model-id.",
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Root directory for evaluation outputs")
    parser.add_argument("--evaluation-set", default=str(DEFAULT_EVALUATION_SET), help="Path to evaluation_set_v2.yaml")
    parser.add_argument("--judge-provider", choices=["dummy", "fugu"], default="dummy", help="Judge provider. dummy performs no network calls.")
    parser.add_argument("--timeout", type=int, default=None, help="Per-request timeout in seconds (overrides FUGU_TIMEOUT_SECONDS).")
    parser.add_argument("--max-retries", type=int, default=None, help="Max additional attempts after the first on transient errors (overrides FUGU_MAX_RETRIES).")
    parser.add_argument("--backoff-base-seconds", type=float, default=None, help="Base seconds for exponential backoff between retries (overrides FUGU_BACKOFF_BASE_SECONDS).")
    parser.add_argument("--only-missing", action="store_true", help="Skip questions whose judgements/<qid>_judgement.json already exists (useful for retrying failed judgements).")
    parser.add_argument("--question-ids", default=None, help="Optional comma-separated subset of question ids to judge.")
    parser.add_argument("--dry-run", action="store_true", help="Only create and count judge_inputs; do not write judgements")
    parser.add_argument("--write-dummy-judgements", action="store_true", help="Write clearly marked dummy judgements for plumbing tests")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing judged.jsonl and per-question judgement files for the targeted questions.")
    args = parser.parse_args()

    output_root = Path(args.output_root)
    run_dir = output_root / args.run_id
    judge_inputs_dir = run_dir / "judge_inputs"
    judgements_dir = run_dir / "judgements"
    judged_path = run_dir / "judged.jsonl"

    if not run_dir.exists():
        print(f"ERROR: run directory not found: {run_dir}", file=sys.stderr)
        return 2
    if (
        judged_path.exists()
        and not args.overwrite
        and not args.dry_run
        and not args.only_missing
        and not args.question_ids
    ):
        print(
            f"ERROR: {judged_path} already exists. Use --overwrite, --only-missing, or --question-ids to update.",
            file=sys.stderr,
        )
        return 2

    prepare_judge_inputs(args.run_id, output_root, Path(args.evaluation_set))

    questions = load_evaluation_questions(Path(args.evaluation_set))
    question_by_id = {str(q["id"]): q for q in questions}
    judge_input_files = sorted(judge_inputs_dir.glob("*_judge.md"))
    print(f"Judge input files: {len(judge_input_files)} -> {judge_inputs_dir}")
    if len(judge_input_files) != len(questions):
        print(f"ERROR: expected {len(questions)} judge inputs, found {len(judge_input_files)}", file=sys.stderr)
        return 1
    if args.dry_run:
        print("Dry-run complete. No judge provider was called and no judgements were written.")
        return 0
    if args.judge_provider == "dummy" and not args.write_dummy_judgements:
        print(
            "ERROR: --judge-provider dummy does not create benchmark judgements by default. Use --dry-run for no-output checks, --write-dummy-judgements for plumbing tests, or --judge-provider fugu for real judging.",
            file=sys.stderr,
        )
        return 2

    manifest = load_manifest(run_dir)
    model_id = args.model_id or str(manifest.get("model_id") or args.run_id)
    judge_model = (
        args.judge_model
        or os.getenv("FUGU_JUDGE_MODEL")
        or os.getenv("FUGU_MODEL")
        or model_id
    )

    provider = None
    if args.judge_provider != "dummy":
        provider = get_provider(
            args.judge_provider,
            judge_model,
            timeout=args.timeout,
            max_retries=args.max_retries,
            backoff_base_seconds=args.backoff_base_seconds,
        )

    judgements_dir.mkdir(parents=True, exist_ok=True)

    filter_ids = _parse_question_id_filter(args.question_ids)
    if filter_ids is not None:
        unknown = filter_ids - set(question_by_id.keys())
        if unknown:
            print(f"ERROR: --question-ids contains unknown ids: {sorted(unknown)}", file=sys.stderr)
            return 2

    targets = []
    for path in judge_input_files:
        qid = path.name.removesuffix("_judge.md")
        if filter_ids is not None and qid not in filter_ids:
            continue
        if args.only_missing and (judgements_dir / f"{qid}_judgement.json").exists():
            continue
        targets.append(path)

    print(f"Judge targets this run: {len(targets)} (model_id={model_id}, judge_model={judge_model})")

    failed = []
    succeeded = []
    skipped = []

    for path in targets:
        qid = path.name.removesuffix("_judge.md")
        per_file = judgements_dir / f"{qid}_judgement.json"
        if per_file.exists() and not (args.overwrite or args.only_missing or args.question_ids):
            skipped.append(qid)
            continue
        question_meta = question_by_id[qid]
        started = utc_now_iso()
        start_time = time.perf_counter()
        try:
            if args.judge_provider == "dummy":
                raw = build_dummy_raw(model_id, question_meta)
                response_model = judge_model
                response_provider = "dummy"
            else:
                assert provider is not None
                prompt = path.read_text(encoding="utf-8")
                response = provider.generate(prompt, system_prompt=SYSTEM_PROMPT)
                raw = extract_json_object(response.text)
                response_model = response.model
                response_provider = response.provider
        except Exception as exc:
            error_message = f"{type(exc).__name__}: {exc}"
            print(f"  [{qid}] FAIL ({error_message})", file=sys.stderr)
            failed.append((qid, error_message))
            continue
        finished = utc_now_iso()
        latency = safe_duration(start_time, time.perf_counter())
        normalized = normalize_judgement(raw, run_id=args.run_id, model_id=model_id, question_meta=question_meta)
        normalized["judge_provider"] = response_provider
        normalized["judge_model"] = response_model
        normalized["judge_prompt_template_version"] = JUDGE_PROMPT_TEMPLATE_VERSION
        normalized["judged_started_at"] = started
        normalized["judged_finished_at"] = finished
        normalized["judge_latency_seconds"] = latency
        per_file.write_text(
            json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        succeeded.append(qid)
        print(f"  [{qid}] OK score={normalized.get('final_score')} ({latency:.2f}s)")

    all_judgements = {}
    for q in questions:
        qid = str(q["id"])
        per_file = judgements_dir / f"{qid}_judgement.json"
        if per_file.exists():
            all_judgements[qid] = json.loads(per_file.read_text(encoding="utf-8"))

    ordered_rows = [all_judgements[str(q["id"])] for q in questions if str(q["id"]) in all_judgements]
    write_jsonl(judged_path, ordered_rows)

    print()
    print(f"This run     -> attempted: {len(targets)}, succeeded: {len(succeeded)}, failed: {len(failed)}, skipped: {len(skipped)}")
    print(f"Aggregate    -> judged.jsonl rows: {len(ordered_rows)} / {len(questions)} -> {judged_path}")
    print(f"Per-question -> judgements files: {len(list(judgements_dir.glob('*_judgement.json')))} -> {judgements_dir}")

    missing_overall = [str(q["id"]) for q in questions if str(q["id"]) not in all_judgements]
    if missing_overall:
        print(f"MISSING judgements ({len(missing_overall)}): {missing_overall}", file=sys.stderr)

    if failed:
        print("FAILED this run:", file=sys.stderr)
        for qid, err in failed:
            print(f"  - {qid}: {err}", file=sys.stderr)
        return 1
    if missing_overall:
        return 1
    if args.judge_provider == "dummy":
        print("WARNING: dummy judgements are plumbing artifacts, not benchmark results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
