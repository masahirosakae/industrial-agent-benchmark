#!/usr/bin/env python3
"""Prepare simple v2.0.0 evaluation predictions from pre-written answers."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DATASET_KEYS = [
    "id",
    "version",
    "domain",
    "category",
    "sub_category",
    "task_type",
    "question",
    "context",
    "choices",
    "answer",
    "rubric",
    "expected_capabilities",
    "difficulty",
    "tags",
    "source",
    "public",
    "requires_external_knowledge",
    "notes",
]

ANSWER_KEYS = {"id", "model_id", "answer"}


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


def validate_dataset(records: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    for index, record in enumerate(records, start=1):
        if list(record.keys()) != DATASET_KEYS:
            raise ValueError(f"dataset line {index}: keys do not match v2 schema")
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id.strip():
            raise ValueError(f"dataset line {index}: id must be a non-empty string")
        if record_id in seen:
            raise ValueError(f"dataset line {index}: duplicate dataset id {record_id}")
        seen.add(record_id)
        for key in ["question", "answer", "rubric"]:
            if not isinstance(record.get(key), str):
                raise ValueError(f"dataset line {index}: {key} must be a string")


def load_answers(path: Path, model_id: str, known_ids: set[str]) -> dict[str, str]:
    answers: dict[str, str] = {}
    unknown: list[str] = []
    for index, record in enumerate(read_jsonl(path), start=1):
        if set(record.keys()) != ANSWER_KEYS:
            raise ValueError(f"answers line {index}: keys must be exactly {sorted(ANSWER_KEYS)}")
        answer_id = record["id"]
        answer_model = record["model_id"]
        answer = record["answer"]
        if not isinstance(answer_id, str) or not answer_id.strip():
            raise ValueError(f"answers line {index}: id must be a non-empty string")
        if not isinstance(answer_model, str) or not answer_model.strip():
            raise ValueError(f"answers line {index}: model_id must be a non-empty string")
        if answer_model != model_id:
            raise ValueError(
                f"answers line {index}: model_id {answer_model!r} does not match CLI model id {model_id!r}"
            )
        if not isinstance(answer, str):
            raise ValueError(f"answers line {index}: answer must be a string")
        if answer_id in answers:
            raise ValueError(f"answers line {index}: duplicate answer id {answer_id}")
        if answer_id not in known_ids:
            unknown.append(answer_id)
        answers[answer_id] = answer
    if unknown:
        raise ValueError(f"answers contain unknown ids not present in dataset: {', '.join(sorted(unknown))}")
    return answers


def write_predictions(
    dataset: list[dict[str, Any]], answers: dict[str, str], model_id: str, output_dir: Path
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "predictions.jsonl"
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        for item in dataset:
            prediction = {
                "id": item["id"],
                "model_id": model_id,
                "question": item["question"],
                "reference_answer": item["answer"],
                "rubric": item["rubric"],
                "prediction": answers.get(item["id"], ""),
                "score": None,
                "score_method": "not_scored",
                "metadata": {},
            }
            f.write(json.dumps(prediction, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run simple v2.0.0 evaluation from pre-written answers.")
    parser.add_argument("--dataset", required=True, help="Path to v2 dataset JSONL, e.g. data/v2/test.jsonl")
    parser.add_argument("--answers", required=True, help="Path to answer JSONL")
    parser.add_argument("--model-id", required=True, help="Public/local model identifier for this run")
    parser.add_argument("--output-dir", required=True, help="Output directory for predictions.jsonl")
    args = parser.parse_args()

    try:
        dataset_path = Path(args.dataset)
        answers_path = Path(args.answers)
        output_dir = Path(args.output_dir)
        dataset = read_jsonl(dataset_path)
        validate_dataset(dataset)
        answers = load_answers(answers_path, args.model_id, {item["id"] for item in dataset})
        out_path = write_predictions(dataset, answers, args.model_id, output_dir)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    missing = len(dataset) - len(answers)
    print(f"Wrote predictions: {out_path}")
    print(f"Questions: {len(dataset)}")
    print(f"Answered: {len(answers)}")
    print(f"Missing: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
