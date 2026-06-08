#!/usr/bin/env python3
"""Validate Industrial Agent Benchmark v2.0.0 HF JSONL records."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_KEYS = [
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

REQUIRED_FIELDS = {
    "id",
    "version",
    "domain",
    "category",
    "sub_category",
    "task_type",
    "question",
    "answer",
    "rubric",
    "difficulty",
    "tags",
}

TASK_TYPES = {
    "short_answer",
    "multiple_choice",
    "structured_reasoning",
    "case_analysis",
    "numeric_reasoning",
}

DIFFICULTIES = {"easy", "medium", "hard", "expert"}

FORBIDDEN_PATTERNS = [
    re.compile(r"\bmodel_[a-d]\b"),
    re.compile(r"results_v2/", re.IGNORECASE),
    re.compile(r"results/", re.IGNORECASE),
    re.compile(r"datasets/results", re.IGNORECASE),
    re.compile(r"judgements/", re.IGNORECASE),
    re.compile(r"judge_outputs", re.IGNORECASE),
]


def is_list_of_strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def record_text(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False).lower()


def validate_record(record: Any, line_no: int, seen_ids: set[str], errors: list[str]) -> None:
    ctx = f"line {line_no}"
    if not isinstance(record, dict):
        errors.append(f"{ctx}: record must be object")
        return

    keys = list(record.keys())
    if keys != SCHEMA_KEYS:
        errors.append(f"{ctx}: keys must exactly match v2 schema")

    for key in REQUIRED_FIELDS:
        value = record.get(key)
        if key == "tags":
            if not is_list_of_strings(value):
                errors.append(f"{ctx}: tags must be list[str]")
            continue
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{ctx}: required field {key} must be non-empty string")

    record_id = record.get("id")
    if isinstance(record_id, str):
        if record_id in seen_ids:
            errors.append(f"{ctx}: duplicate id {record_id}")
        seen_ids.add(record_id)

    string_fields = [
        "id",
        "version",
        "domain",
        "category",
        "sub_category",
        "task_type",
        "question",
        "context",
        "answer",
        "rubric",
        "difficulty",
        "source",
        "notes",
    ]
    for key in string_fields:
        if key in record and not isinstance(record[key], str):
            errors.append(f"{ctx}: {key} must be string")

    for key in ["choices", "expected_capabilities", "tags"]:
        if key in record and not is_list_of_strings(record[key]):
            errors.append(f"{ctx}: {key} must be list[str]")

    for key in ["public", "requires_external_knowledge"]:
        if key in record and not isinstance(record[key], bool):
            errors.append(f"{ctx}: {key} must be bool")

    if record.get("task_type") not in TASK_TYPES:
        errors.append(f"{ctx}: invalid task_type {record.get('task_type')!r}")
    if record.get("difficulty") not in DIFFICULTIES:
        errors.append(f"{ctx}: invalid difficulty {record.get('difficulty')!r}")
    if record.get("version") != "2.0.0":
        errors.append(f"{ctx}: version must be '2.0.0'")

    lowered = record_text(record)
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(lowered):
            errors.append(f"{ctx}: forbidden private/evaluation artifact reference")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate v2.0.0 HF dataset JSONL.")
    parser.add_argument("jsonl_path", help="Path to JSONL file, e.g. data/v2/test.jsonl")
    args = parser.parse_args()

    path = Path(args.jsonl_path)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    errors: list[str] = []
    seen_ids: set[str] = set()
    count = 0
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                errors.append(f"line {line_no}: blank lines are not allowed")
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: JSON parse error: {exc}")
                continue
            validate_record(record, line_no, seen_ids, errors)
            count += 1

    print(f"Checked: {count} records")
    print(f"Errors:  {len(errors)}")
    for error in errors:
        print(f"  ERR  {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
