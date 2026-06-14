#!/usr/bin/env python3
"""Aggregate Judge v2 JSONL results into CSV metrics and a Markdown report."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from eval_v2_common import (
    GROUPED_METRIC_COLUMNS,
    LEADERBOARD_COLUMNS,
    METRIC_COLUMNS,
    compute_metric_row,
    group_rows,
    normalize_bool,
    normalize_float,
    read_jsonl,
    write_csv,
)


def load_run_id_model_id(run_dir: Path, rows: list[dict[str, Any]]) -> tuple[str, str]:
    manifest_path = run_dir / "manifest.json"
    manifest: dict[str, Any] = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    run_id = str(manifest.get("run_id") or (rows[0].get("run_id") if rows else run_dir.name))
    model_id = str(manifest.get("model_id") or (rows[0].get("model_id") if rows else run_dir.name))
    return run_id, model_id


def grouped_metric_rows(rows: list[dict[str, Any]], *, run_id: str, model_id: str, group_type: str, key: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for group_value, group in sorted(group_rows(rows, key).items(), key=lambda item: item[0]):
        row = {"group_type": group_type, "group_value": group_value}
        row.update(compute_metric_row(group, run_id=run_id, model_id=model_id))
        out.append(row)
    return out


def failure_rows(rows: list[dict[str, Any]], *, run_id: str, model_id: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        out.append(
            {
                "run_id": run_id,
                "model_id": model_id,
                "question_id": row.get("question_id", ""),
                "layer": row.get("layer", ""),
                "category": row.get("category", ""),
                "difficulty": row.get("difficulty", ""),
                "domain": row.get("domain", ""),
                "final_score": row.get("final_score", ""),
                "critical_failure_triggered": normalize_bool(row.get("critical_failure_triggered")),
                "score_cap_applied": normalize_bool(row.get("score_cap_applied")),
                "generic_penalty_triggered": normalize_bool(row.get("generic_penalty_triggered")),
                "numeric_check_failed_ratio": normalize_float(row.get("numeric_check_failed_ratio")),
                "structured_output_missing_count": row.get("structured_output_missing_count", 0),
                "judge_summary": row.get("judge_summary", ""),
            }
        )
    return out


def render_report(run_dir: Path, overall: dict[str, Any], grouped: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# Industrial Agent Benchmark v1.1.0-pre Evaluation Report",
        "",
        f"- Run ID: `{overall['run_id']}`",
        f"- Model ID: `{overall['model_id']}`",
        f"- Questions: {overall['question_count']}",
        f"- Average final score: {overall['avg_final_score']}",
        f"- Score range: {overall['min_score']}?{overall['max_score']}",
        f"- Critical failure rate: {overall['critical_failure_rate']}",
        f"- Score cap rate: {overall['score_cap_rate']}",
        f"- Generic penalty rate: {overall['generic_penalty_rate']}",
        f"- Average numeric check failed ratio: {overall['avg_numeric_check_failed_ratio']}",
        f"- Structured output failure rate: {overall['structured_output_failure_rate']}",
        "",
    ]
    for title, rows in grouped.items():
        lines.append(f"## {title}")
        lines.append("")
        lines.append("| group | n | avg | critical_rate | cap_rate | generic_rate | numeric_failed_avg |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for row in rows:
            lines.append(
                f"| {row['group_value']} | {row['question_count']} | {row['avg_final_score']} | "
                f"{row['critical_failure_rate']} | {row['score_cap_rate']} | {row['generic_penalty_rate']} | "
                f"{row['avg_numeric_check_failed_ratio']} |"
            )
        lines.append("")
    lines.append(f"CSV metrics are written under `{run_dir / 'metrics'}`.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate v1.1 Judge v2 results.")
    parser.add_argument("--run-dir", required=True, help="Run directory containing judged.jsonl")
    parser.add_argument("--judged-file", default=None, help="Optional path to judged.jsonl")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    judged_path = Path(args.judged_file) if args.judged_file else run_dir / "judged.jsonl"
    if not judged_path.exists():
        print(f"ERROR: judged JSONL not found: {judged_path}", file=sys.stderr)
        return 2

    rows = read_jsonl(judged_path)
    run_id, model_id = load_run_id_model_id(run_dir, rows)
    metrics_dir = run_dir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    overall = compute_metric_row(rows, run_id=run_id, model_id=model_id)
    layer_rows = grouped_metric_rows(rows, run_id=run_id, model_id=model_id, group_type="layer", key="layer")
    category_rows = grouped_metric_rows(rows, run_id=run_id, model_id=model_id, group_type="category", key="category")
    difficulty_rows = grouped_metric_rows(rows, run_id=run_id, model_id=model_id, group_type="difficulty", key="difficulty")
    failures = failure_rows(rows, run_id=run_id, model_id=model_id)

    write_csv(metrics_dir / "overall.csv", [overall], METRIC_COLUMNS)
    write_csv(metrics_dir / "layer.csv", layer_rows, GROUPED_METRIC_COLUMNS)
    write_csv(metrics_dir / "category.csv", category_rows, GROUPED_METRIC_COLUMNS)
    write_csv(metrics_dir / "difficulty.csv", difficulty_rows, GROUPED_METRIC_COLUMNS)
    write_csv(
        metrics_dir / "failure_analysis.csv",
        failures,
        [
            "run_id",
            "model_id",
            "question_id",
            "layer",
            "category",
            "difficulty",
            "domain",
            "final_score",
            "critical_failure_triggered",
            "score_cap_applied",
            "generic_penalty_triggered",
            "numeric_check_failed_ratio",
            "structured_output_missing_count",
            "judge_summary",
        ],
    )
    write_csv(run_dir / "leaderboard_v2.csv", rows, LEADERBOARD_COLUMNS)

    report = render_report(
        run_dir,
        overall,
        {"Layer": layer_rows, "Category": category_rows, "Difficulty": difficulty_rows},
    )
    (run_dir / "report.md").write_text(report, encoding="utf-8", newline="\n")

    print(f"Aggregated rows: {len(rows)}")
    print(f"Metrics directory: {metrics_dir}")
    print(f"Report: {run_dir / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
