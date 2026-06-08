#!/usr/bin/env python3
"""Run deterministic rule-based Judge Evaluation v2 over simple predictions."""
from __future__ import annotations

import argparse
import json
import re
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

SCORE_METHOD = "rule_based_token_overlap_v1"
TOKEN_RE = re.compile(r"[A-Za-z0-9_]{3,}")


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
            records.append(record)
    return records


def validate_prediction(record: dict[str, Any], index: int) -> None:
    if list(record.keys()) != PREDICTION_KEYS:
        raise ValueError(f"prediction line {index}: keys do not match prediction schema")
    for key in ["id", "model_id", "question", "reference_answer", "rubric", "prediction", "score_method"]:
        if not isinstance(record.get(key), str):
            raise ValueError(f"prediction line {index}: {key} must be a string")
    if record.get("score") is not None:
        raise ValueError(f"prediction line {index}: score must be null before judge evaluation")
    if record.get("score_method") != "not_scored":
        raise ValueError(f"prediction line {index}: score_method must be 'not_scored'")
    if not isinstance(record.get("metadata"), dict):
        raise ValueError(f"prediction line {index}: metadata must be an object")


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def score_prediction(prediction: str, reference_answer: str, rubric: str) -> tuple[int, dict[str, Any]]:
    prediction = prediction.strip()
    if not prediction:
        return 0, {
            "reason": "missing_prediction",
            "prediction_token_count": 0,
            "reference_token_count": 0,
            "overlap_count": 0,
            "overlap_ratio": 0.0,
        }

    pred_tokens = tokenize(prediction)
    ref_tokens = tokenize(reference_answer + "\n" + rubric)
    overlap = pred_tokens & ref_tokens
    if not pred_tokens or not ref_tokens:
        return 1, {
            "reason": "insufficient_tokens_for_overlap",
            "prediction_token_count": len(pred_tokens),
            "reference_token_count": len(ref_tokens),
            "overlap_count": len(overlap),
            "overlap_ratio": 0.0,
        }

    overlap_ratio = len(overlap) / min(len(pred_tokens), len(ref_tokens))
    if overlap_ratio >= 0.75:
        score = 5
    elif overlap_ratio >= 0.50:
        score = 4
    elif overlap_ratio >= 0.30:
        score = 3
    elif overlap_ratio >= 0.15:
        score = 2
    else:
        score = 1

    return score, {
        "reason": "token_overlap",
        "prediction_token_count": len(pred_tokens),
        "reference_token_count": len(ref_tokens),
        "overlap_count": len(overlap),
        "overlap_ratio": round(overlap_ratio, 4),
        "matched_terms": sorted(overlap)[:25],
    }


def build_judgement(record: dict[str, Any]) -> dict[str, Any]:
    score, metadata = score_prediction(record["prediction"], record["reference_answer"], record["rubric"])
    judgement = {
        "id": record["id"],
        "model_id": record["model_id"],
        "score": score,
        "score_method": SCORE_METHOD,
        "prediction": record["prediction"],
        "reference_answer": record["reference_answer"],
        "rubric": record["rubric"],
        "metadata": metadata,
    }
    return {key: judgement[key] for key in JUDGEMENT_KEYS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic rule-based Judge Evaluation v2.")
    parser.add_argument("--predictions", required=True, help="Path to simple-eval predictions.jsonl")
    parser.add_argument("--output-dir", required=True, help="Output directory for judgements.jsonl")
    args = parser.parse_args()

    try:
        predictions = read_jsonl(Path(args.predictions))
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / "judgements.jsonl"
        with out_path.open("w", encoding="utf-8", newline="\n") as f:
            for index, record in enumerate(predictions, start=1):
                validate_prediction(record, index)
                judgement = build_judgement(record)
                f.write(json.dumps(judgement, ensure_ascii=False, separators=(",", ":")))
                f.write("\n")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote judgements: {out_path}")
    print(f"Judged: {len(predictions)}")
    print(f"Score method: {SCORE_METHOD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
