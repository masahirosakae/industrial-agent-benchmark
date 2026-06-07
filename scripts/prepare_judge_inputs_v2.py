#!/usr/bin/env python3
"""Prepare Industrial Agent Benchmark v1.1 Judge v2 inputs.

This script reads model answers from:
  results_v2/<model_id>/answers/<question_id>.txt

and writes Judge prompts to:
  results_v2/<model_id>/judge_inputs/<question_id>_judge.md

It does not call any model or judge. It only materializes judge input files.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RESULTS_ROOT = ROOT / "results_v2"
EVAL_SET_PATH = ROOT / "evaluation_set_v2.yaml"
INDEX_PATH = ROOT / "benchmark_data" / "index.yaml"
JUDGE_TEMPLATE_PATH = ROOT / "judge_template_v2.md"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def bullet_list(items: list[Any]) -> str:
    if not items:
        return "- (none)"
    return "\n".join(f"- {item}" for item in items)


def yaml_block(value: Any) -> str:
    if value is None:
        return "```yaml\nnull\n```"
    dumped = yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120).rstrip()
    return f"```yaml\n{dumped}\n```"


def render_template(template: str, replacements: dict[str, str]) -> str:
    """Replace {tokens} without using str.format, because the template contains JSON braces."""
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace("{" + key + "}", value)
    return rendered


def problem_path_from_index(index_by_id: dict[str, dict[str, Any]], question_id: str) -> Path:
    item = index_by_id.get(question_id)
    if not item:
        raise KeyError(f"question_id {question_id} not found in benchmark_data/index.yaml")
    return ROOT / item["file_path"]


def build_judge_input(question_id: str, problem: dict[str, Any], model_answer: str, template: str) -> str:
    rubric = problem.get("evaluation_rubric", {}) or {}
    replacements = {
        "question_id": str(problem.get("id", question_id)),
        "layer": str(problem.get("layer", "")),
        "category": str(problem.get("category", "")),
        "domain": str(problem.get("domain", "")),
        "subdomain": str(problem.get("subdomain", "")),
        "difficulty": str(problem.get("difficulty", "")),
        "primary_skill": str(problem.get("primary_skill", "")),
        "schema_version": str(problem.get("schema_version", "1.0")),
        "scenario": str(problem.get("scenario", "")),
        "question": str(problem.get("question", "")),
        "reference_answer": str(problem.get("reference_answer", "")),
        "must_have": bullet_list(rubric.get("must_have", []) or []),
        "nice_to_have": bullet_list(rubric.get("nice_to_have", []) or []),
        "critical_failures": bullet_list(rubric.get("critical_failures", []) or []),
        "score_cap_rules": yaml_block(problem.get("score_cap_rules", [])),
        "numeric_checks": yaml_block(problem.get("numeric_checks", [])),
        "generic_answer_penalty": yaml_block(problem.get("generic_answer_penalty", {})),
        "structured_output_requirements": yaml_block(problem.get("structured_output_requirements", {})),
        "disallowed_answers": yaml_block(problem.get("disallowed_answers", [])),
        "model_answer": model_answer,
    }
    return render_template(template, replacements)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare Judge v2 input markdown files for one model.")
    parser.add_argument("model_id", help="Neutral model directory id, e.g. model_a")
    parser.add_argument("--results-root", default=str(DEFAULT_RESULTS_ROOT), help="Path to results_v2 root")
    parser.add_argument("--evaluation-set", default=str(EVAL_SET_PATH), help="Path to evaluation_set_v2.yaml")
    parser.add_argument("--judge-template", default=str(JUDGE_TEMPLATE_PATH), help="Path to judge_template_v2.md")
    parser.add_argument("--allow-missing", action="store_true", help="Skip missing answer files instead of failing")
    args = parser.parse_args()

    results_root = Path(args.results_root)
    model_dir = results_root / args.model_id
    answers_dir = model_dir / "answers"
    judge_inputs_dir = model_dir / "judge_inputs"
    if not answers_dir.exists():
        print(f"ERROR: answers directory not found: {answers_dir}", file=sys.stderr)
        return 2
    judge_inputs_dir.mkdir(parents=True, exist_ok=True)

    eval_set = load_yaml(Path(args.evaluation_set))
    index = load_yaml(INDEX_PATH)
    index_by_id = {item["id"]: item for item in index.get("items", [])}
    template = Path(args.judge_template).read_text(encoding="utf-8")

    created = 0
    missing: list[str] = []
    for q in eval_set.get("questions", []):
        question_id = q["id"]
        answer_path = answers_dir / f"{question_id}.txt"
        if not answer_path.exists():
            missing.append(question_id)
            if args.allow_missing:
                continue
            continue
        model_answer = answer_path.read_text(encoding="utf-8").strip()
        if not model_answer:
            missing.append(question_id)
            if args.allow_missing:
                continue
            continue
        problem = load_yaml(problem_path_from_index(index_by_id, question_id))
        judge_input = build_judge_input(question_id, problem, model_answer, template)
        out_path = judge_inputs_dir / f"{question_id}_judge.md"
        out_path.write_text(judge_input, encoding="utf-8", newline="\n")
        created += 1

    if missing and not args.allow_missing:
        print("ERROR: missing or empty answer files:", file=sys.stderr)
        for qid in missing:
            print(f"  - {answers_dir / (qid + '.txt')}", file=sys.stderr)
        print(f"Created {created} judge input files before detecting missing answers.", file=sys.stderr)
        return 1

    print(f"Created judge input files: {created}")
    if missing:
        print(f"Skipped missing/empty answers: {len(missing)}")
    print(f"Output directory: {judge_inputs_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
