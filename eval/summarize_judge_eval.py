#!/usr/bin/env python3
"""Summarize deterministic Judge Evaluation v2 judgements."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

JUDGEMENT_KEYS = [
    "id",
    "model_id",
    "score",
    "score_method",
    "prediction",
    "reference_answer",
    "rubric",
    "metadata",
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
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
            if list(record.keys()) != JUDGEMENT_KEYS:
                raise ValueError(f"{path}: line {line_no}: keys do not match judgement schema")
            score = record.get("score")
            if not isinstance(score, int) or isinstance(score, bool) or score < 0 or score > 5:
                raise ValueError(f"{path}: line {line_no}: score must be an integer 0..5")
            if not isinstance(record.get("metadata"), dict):
                raise ValueError(f"{path}: line {line_no}: metadata must be an object")
            records.append(record)
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        raise ValueError("judgements file contains no records")
    model_ids = {record["model_id"] for record in records}
    if len(model_ids) != 1:
        raise ValueError(f"judgements contain multiple model_id values: {sorted(model_ids)}")
    score_methods = {record["score_method"] for record in records}
    if len(score_methods) != 1:
        raise ValueError(f"judgements contain multiple score_method values: {sorted(score_methods)}")

    scores = [record["score"] for record in records]
    answered = sum(1 for record in records if record["prediction"].strip())
    distribution = Counter(scores)
    return {
        "model_id": next(iter(model_ids)),
        "num_questions": len(records),
        "num_answered": answered,
        "num_missing": len(records) - answered,
        "score_method": next(iter(score_methods)),
        "average_score": round(sum(scores) / len(scores), 4),
        "min_score": min(scores),
        "max_score": max(scores),
        "score_distribution": {str(score): distribution.get(score, 0) for score in range(0, 6)},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize deterministic Judge Evaluation v2 results.")
    parser.add_argument("--judgements", required=True, help="Path to judgements.jsonl")
    parser.add_argument("--output", required=True, help="Path to summary.json")
    args = parser.parse_args()

    try:
        summary = summarize(read_jsonl(Path(args.judgements)))
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
