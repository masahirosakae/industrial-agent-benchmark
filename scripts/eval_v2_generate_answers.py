#!/usr/bin/env python3
"""Generate answer prompts and raw answers for evaluation_set_v2.

No network calls are made when --dry-run is set or --provider dummy is used.
Real model execution is opt-in via --provider fugu.
"""
from __future__ import annotations

import argparse
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
    render_answer_prompt,
    safe_duration,
    utc_now_iso,
    write_jsonl,
)

SYSTEM_PROMPT = (
    "You are answering Industrial Agent Benchmark v1.1.0-pre tasks. "
    "Answer in Japanese. If the question requests JSON, return valid JSON only when possible."
)


def build_manifest(args: argparse.Namespace, question_count: int, leakage_count: int) -> dict[str, Any]:
    return {
        "run_id": args.run_id,
        "model_id": args.model_id,
        "provider": args.provider,
        "benchmark_version": "v1.1.0-pre",
        "evaluation_set": str(args.evaluation_set),
        "question_count": question_count,
        "temperature": 0,
        "prompt_template_version": ANSWER_PROMPT_TEMPLATE_VERSION,
        "created_at": utc_now_iso(),
        "dry_run": bool(args.dry_run),
        "prompt_leakage_count": leakage_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate raw answers for Industrial Agent Benchmark evaluation_set_v2.")
    parser.add_argument("--run-id", required=True, help="Run directory id under --output-root")
    parser.add_argument("--model-id", required=True, help="Neutral model id recorded in JSONL")
    parser.add_argument("--provider", choices=["dummy", "fugu"], default="dummy", help="Model provider. dummy performs no network calls.")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Root directory for evaluation outputs")
    parser.add_argument("--evaluation-set", default=str(DEFAULT_EVALUATION_SET), help="Path to evaluation_set_v2.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Render prompts and write placeholder answers without provider calls")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing answers.jsonl and per-question answers")
    args = parser.parse_args()

    output_root = Path(args.output_root)
    run_dir = output_root / args.run_id
    answers_dir = run_dir / "answers"
    prompts_path = run_dir / "prompts.jsonl"
    answers_path = run_dir / "answers.jsonl"
    manifest_path = run_dir / "manifest.json"

    if run_dir.exists() and answers_path.exists() and not args.overwrite:
        print(f"ERROR: {answers_path} already exists. Use --overwrite to replace it.", file=sys.stderr)
        return 2

    questions = load_evaluation_questions(Path(args.evaluation_set))
    index_by_id = load_index_by_id()
    provider = None if args.dry_run else get_provider(args.provider, args.model_id)

    run_dir.mkdir(parents=True, exist_ok=True)
    answers_dir.mkdir(parents=True, exist_ok=True)

    prompt_rows: list[dict[str, Any]] = []
    answer_rows: list[dict[str, Any]] = []
    leakage_issues: dict[str, list[str]] = {}

    for q in questions:
        qid = str(q["id"])
        problem = load_problem(qid, index_by_id)
        prompt = render_answer_prompt(q, problem)
        leaked_terms = check_prompt_leakage(prompt)
        if leaked_terms:
            leakage_issues[qid] = leaked_terms

        prompt_rows.append(
            {
                "run_id": args.run_id,
                "question_id": qid,
                "layer": problem.get("layer", q.get("layer", "")),
                "category": problem.get("category", q.get("category", "")),
                "difficulty": problem.get("difficulty", q.get("difficulty", "")),
                "domain": problem.get("domain", q.get("domain", "")),
                "prompt": prompt,
                "prompt_template_version": ANSWER_PROMPT_TEMPLATE_VERSION,
            }
        )

        started = utc_now_iso()
        start_time = time.perf_counter()
        error = ""
        if args.dry_run:
            answer_text = (
                "Dry-run placeholder answer. "
                "For real evaluation, set --provider fugu and run under identical conditions."
            )
            provider_name = "dry_run"
            provider_model = args.model_id
        else:
            try:
                assert provider is not None
                response = provider.generate(prompt, system_prompt=SYSTEM_PROMPT)
                answer_text = response.text.strip()
                provider_name = response.provider
                provider_model = response.model
            except Exception as exc:  # noqa: BLE001 - preserve error per row for reproducibility
                answer_text = ""
                error = f"{type(exc).__name__}: {exc}"
                provider_name = args.provider
                provider_model = args.model_id
        end_time = time.perf_counter()
        finished = utc_now_iso()
        latency = safe_duration(start_time, end_time)

        (answers_dir / f"{qid}.txt").write_text(answer_text, encoding="utf-8", newline="\n")
        answer_rows.append(
            {
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
        )

    write_jsonl(prompts_path, prompt_rows)
    write_jsonl(answers_path, answer_rows)
    manifest = build_manifest(args, len(questions), sum(len(v) for v in leakage_issues.values()))
    import json

    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"Run directory: {run_dir}")
    print(f"Prompts written: {len(prompt_rows)} -> {prompts_path}")
    print(f"Answers written: {len(answer_rows)} -> {answers_path}")
    print(f"Per-question answer files: {len(list(answers_dir.glob('*.txt')))} -> {answers_dir}")
    if leakage_issues:
        print("ERROR: prompt leakage detected:", file=sys.stderr)
        for qid, terms in leakage_issues.items():
            print(f"  - {qid}: {', '.join(terms)}", file=sys.stderr)
        return 1
    print("Prompt leakage check: 0 forbidden terms")
    if any(row["error"] for row in answer_rows):
        print("ERROR: one or more answer generations failed. See answers.jsonl error fields.", file=sys.stderr)
        return 1
    if args.dry_run or args.provider == "dummy":
        print("No benchmark model run was executed (dry-run/dummy mode).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
