#!/usr/bin/env python3
"""Compare two Industrial Agent Benchmark v1.1 evaluation runs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from eval_v2_common import (
    compute_metric_row,
    group_rows,
    normalize_bool,
    normalize_float,
    read_jsonl,
    write_csv,
)

COMPARISON_COLUMNS = [
    "group_type",
    "group_value",
    "left_label",
    "right_label",
    "left_question_count",
    "right_question_count",
    "left_avg_score",
    "right_avg_score",
    "delta_right_minus_left",
    "left_critical_failure_rate",
    "right_critical_failure_rate",
    "left_score_cap_rate",
    "right_score_cap_rate",
    "left_generic_penalty_rate",
    "right_generic_penalty_rate",
    "left_avg_numeric_check_failed_ratio",
    "right_avg_numeric_check_failed_ratio",
    "left_structured_output_failure_rate",
    "right_structured_output_failure_rate",
]

FAILURE_COMPARISON_COLUMNS = [
    "question_id",
    "layer",
    "category",
    "difficulty",
    "domain",
    "left_label",
    "right_label",
    "left_final_score",
    "right_final_score",
    "delta_right_minus_left",
    "left_critical_failure_triggered",
    "right_critical_failure_triggered",
    "left_score_cap_applied",
    "right_score_cap_applied",
    "left_generic_penalty_triggered",
    "right_generic_penalty_triggered",
    "left_numeric_check_failed_ratio",
    "right_numeric_check_failed_ratio",
]


def load_rows(run_dir: Path) -> list[dict[str, Any]]:
    judged_path = run_dir / "judged.jsonl"
    if not judged_path.exists():
        raise FileNotFoundError(f"judged.jsonl not found: {judged_path}")
    return read_jsonl(judged_path)


def run_id_model_id(run_dir: Path, rows: list[dict[str, Any]]) -> tuple[str, str]:
    manifest_path = run_dir / "manifest.json"
    manifest: dict[str, Any] = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return (
        str(manifest.get("run_id") or (rows[0].get("run_id") if rows else run_dir.name)),
        str(manifest.get("model_id") or (rows[0].get("model_id") if rows else run_dir.name)),
    )


def compare_metric(left_metric: dict[str, Any], right_metric: dict[str, Any], *, group_type: str, group_value: str, left_label: str, right_label: str) -> dict[str, Any]:
    left_avg = normalize_float(left_metric.get("avg_final_score"))
    right_avg = normalize_float(right_metric.get("avg_final_score"))
    return {
        "group_type": group_type,
        "group_value": group_value,
        "left_label": left_label,
        "right_label": right_label,
        "left_question_count": left_metric.get("question_count", 0),
        "right_question_count": right_metric.get("question_count", 0),
        "left_avg_score": left_avg,
        "right_avg_score": right_avg,
        "delta_right_minus_left": round(right_avg - left_avg, 4),
        "left_critical_failure_rate": left_metric.get("critical_failure_rate", 0),
        "right_critical_failure_rate": right_metric.get("critical_failure_rate", 0),
        "left_score_cap_rate": left_metric.get("score_cap_rate", 0),
        "right_score_cap_rate": right_metric.get("score_cap_rate", 0),
        "left_generic_penalty_rate": left_metric.get("generic_penalty_rate", 0),
        "right_generic_penalty_rate": right_metric.get("generic_penalty_rate", 0),
        "left_avg_numeric_check_failed_ratio": left_metric.get("avg_numeric_check_failed_ratio", 0),
        "right_avg_numeric_check_failed_ratio": right_metric.get("avg_numeric_check_failed_ratio", 0),
        "left_structured_output_failure_rate": left_metric.get("structured_output_failure_rate", 0),
        "right_structured_output_failure_rate": right_metric.get("structured_output_failure_rate", 0),
    }


def compare_overall(left_rows: list[dict[str, Any]], right_rows: list[dict[str, Any]], *, left_label: str, right_label: str) -> list[dict[str, Any]]:
    left_metric = compute_metric_row(left_rows, run_id=left_label, model_id=left_label)
    right_metric = compute_metric_row(right_rows, run_id=right_label, model_id=right_label)
    return [compare_metric(left_metric, right_metric, group_type="overall", group_value="all", left_label=left_label, right_label=right_label)]


def compare_group(left_rows: list[dict[str, Any]], right_rows: list[dict[str, Any]], *, key: str, group_type: str, left_label: str, right_label: str) -> list[dict[str, Any]]:
    left_groups = group_rows(left_rows, key)
    right_groups = group_rows(right_rows, key)
    all_values = sorted(set(left_groups) | set(right_groups))
    out: list[dict[str, Any]] = []
    for value in all_values:
        left_metric = compute_metric_row(left_groups.get(value, []), run_id=left_label, model_id=left_label)
        right_metric = compute_metric_row(right_groups.get(value, []), run_id=right_label, model_id=right_label)
        out.append(compare_metric(left_metric, right_metric, group_type=group_type, group_value=value, left_label=left_label, right_label=right_label))
    return out


def compare_failures(left_rows: list[dict[str, Any]], right_rows: list[dict[str, Any]], *, left_label: str, right_label: str) -> list[dict[str, Any]]:
    left_by_qid = {str(row.get("question_id")): row for row in left_rows}
    right_by_qid = {str(row.get("question_id")): row for row in right_rows}
    out: list[dict[str, Any]] = []
    for qid in sorted(set(left_by_qid) | set(right_by_qid)):
        left = left_by_qid.get(qid, {})
        right = right_by_qid.get(qid, {})
        left_score = normalize_float(left.get("final_score"))
        right_score = normalize_float(right.get("final_score"))
        meta = left or right
        out.append(
            {
                "question_id": qid,
                "layer": meta.get("layer", ""),
                "category": meta.get("category", ""),
                "difficulty": meta.get("difficulty", ""),
                "domain": meta.get("domain", ""),
                "left_label": left_label,
                "right_label": right_label,
                "left_final_score": left_score,
                "right_final_score": right_score,
                "delta_right_minus_left": round(right_score - left_score, 4),
                "left_critical_failure_triggered": normalize_bool(left.get("critical_failure_triggered")),
                "right_critical_failure_triggered": normalize_bool(right.get("critical_failure_triggered")),
                "left_score_cap_applied": normalize_bool(left.get("score_cap_applied")),
                "right_score_cap_applied": normalize_bool(right.get("score_cap_applied")),
                "left_generic_penalty_triggered": normalize_bool(left.get("generic_penalty_triggered")),
                "right_generic_penalty_triggered": normalize_bool(right.get("generic_penalty_triggered")),
                "left_numeric_check_failed_ratio": normalize_float(left.get("numeric_check_failed_ratio")),
                "right_numeric_check_failed_ratio": normalize_float(right.get("numeric_check_failed_ratio")),
            }
        )
    return out


def render_report(overall: list[dict[str, Any]], layer: list[dict[str, Any]], category: list[dict[str, Any]], difficulty: list[dict[str, Any]]) -> str:
    top = overall[0]
    left_label = top["left_label"]
    right_label = top["right_label"]
    lines = [
        "# Industrial Agent Benchmark v1.1.0-pre Comparison Report",
        "",
        f"- Left run: `{left_label}`",
        f"- Right run: `{right_label}`",
        f"- Overall average ({left_label}): {top['left_avg_score']}",
        f"- Overall average ({right_label}): {top['right_avg_score']}",
        f"- Delta right minus left: {top['delta_right_minus_left']}",
        "",
        "## Layer comparison",
        "",
        "| layer | left_avg | right_avg | delta | left_cap_rate | right_cap_rate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in layer:
        lines.append(f"| {row['group_value']} | {row['left_avg_score']} | {row['right_avg_score']} | {row['delta_right_minus_left']} | {row['left_score_cap_rate']} | {row['right_score_cap_rate']} |")
    lines.extend(["", "## Category comparison", "", "| category | left_avg | right_avg | delta |", "|---|---:|---:|---:|"])
    for row in category:
        lines.append(f"| {row['group_value']} | {row['left_avg_score']} | {row['right_avg_score']} | {row['delta_right_minus_left']} |")
    lines.extend(["", "## Difficulty comparison", "", "| difficulty | left_avg | right_avg | delta |", "|---|---:|---:|---:|"])
    for row in difficulty:
        lines.append(f"| {row['group_value']} | {row['left_avg_score']} | {row['right_avg_score']} | {row['delta_right_minus_left']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two v1.1 evaluation runs.")
    parser.add_argument("--left", required=True, help="Left run directory")
    parser.add_argument("--right", required=True, help="Right run directory")
    parser.add_argument("--left-label", default=None, help="Display label for left run")
    parser.add_argument("--right-label", default=None, help="Display label for right run")
    parser.add_argument("--output-dir", required=True, help="Directory for comparison CSV/Markdown outputs")
    parser.add_argument("--report-name", default="fugu_mini_vs_ultra_report.md", help="Markdown report filename")
    args = parser.parse_args()

    left_dir = Path(args.left)
    right_dir = Path(args.right)
    output_dir = Path(args.output_dir)
    try:
        left_rows = load_rows(left_dir)
        right_rows = load_rows(right_dir)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    left_run_id, left_model_id = run_id_model_id(left_dir, left_rows)
    right_run_id, right_model_id = run_id_model_id(right_dir, right_rows)
    left_label = args.left_label or left_model_id or left_run_id
    right_label = args.right_label or right_model_id or right_run_id

    output_dir.mkdir(parents=True, exist_ok=True)
    overall = compare_overall(left_rows, right_rows, left_label=left_label, right_label=right_label)
    layer = compare_group(left_rows, right_rows, key="layer", group_type="layer", left_label=left_label, right_label=right_label)
    category = compare_group(left_rows, right_rows, key="category", group_type="category", left_label=left_label, right_label=right_label)
    difficulty = compare_group(left_rows, right_rows, key="difficulty", group_type="difficulty", left_label=left_label, right_label=right_label)
    failures = compare_failures(left_rows, right_rows, left_label=left_label, right_label=right_label)

    write_csv(output_dir / "overall_comparison.csv", overall, COMPARISON_COLUMNS)
    write_csv(output_dir / "layer_comparison.csv", layer, COMPARISON_COLUMNS)
    write_csv(output_dir / "category_comparison.csv", category, COMPARISON_COLUMNS)
    write_csv(output_dir / "difficulty_comparison.csv", difficulty, COMPARISON_COLUMNS)
    write_csv(output_dir / "failure_analysis.csv", failures, FAILURE_COMPARISON_COLUMNS)
    report = render_report(overall, layer, category, difficulty)
    (output_dir / args.report_name).write_text(report, encoding="utf-8", newline="\n")

    print(f"Comparison output: {output_dir}")
    print(f"Overall delta right-left: {overall[0]['delta_right_minus_left']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
