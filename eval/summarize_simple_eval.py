#!/usr/bin/env python3
"""Summarize simple v2.0.0 evaluation predictions."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PREDICTION_KEYS = [
    "id",
    "model_id",
    "question",
    "reference_answer",
    "rubric",
    "prediction",
    "score",
    "score_method",
    "metadata",
]


def read_predictions(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                raise ValueError(f"{path}: line {line_no}: blank lines are not allowed")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}: line {line_no}: JSON parse error: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}: line {line_no}: record must be an object")
            if list(record.keys()) != PREDICTION_KEYS:
                raise ValueError(f"{path}: line {line_no}: keys do not match prediction schema")
            if record.get("score_method") != "not_scored":
                raise ValueError(f"{path}: line {line_no}: score_method must be 'not_scored'")
            if record.get("score") is not None:
                raise ValueError(f"{path}: line {line_no}: score must be null")
            if not isinstance(record.get("prediction"), str):
                raise ValueError(f"{path}: line {line_no}: prediction must be a string")
            records.append(record)
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        raise ValueError("predictions file contains no records")
    model_ids = {record["model_id"] for record in records}
    if len(model_ids) != 1:
        raise ValueError(f"predictions contain multiple model_id values: {sorted(model_ids)}")
    num_answered = sum(1 for record in records if record["prediction"].strip())
    return {
        "model_id": next(iter(model_ids)),
        "num_questions": len(records),
        "num_answered": num_answered,
        "num_missing": len(records) - num_answered,
        "score_method": "not_scored",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize simple v2.0.0 evaluation predictions.")
    parser.add_argument("--predictions", required=True, help="Path to predictions.jsonl")
    parser.add_argument("--output", required=True, help="Path to summary.json")
    args = parser.parse_args()

    try:
        summary = summarize(read_predictions(Path(args.predictions)))
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote summary: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
