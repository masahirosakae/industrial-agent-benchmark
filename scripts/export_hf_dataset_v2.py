#!/usr/bin/env python3
"""Export public benchmark YAML files to the v2.0.0 HF JSONL schema."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "benchmark_data"
OUT_PATH = ROOT / "data" / "v2" / "test.jsonl"

VERSION = "2.0.0"
DOMAIN = "manufacturing"
SOURCE = "synthetic"

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

LAYER_TO_CATEGORY = {
    "industrial_knowledge": "knowledge",
    "industrial_reasoning": "reasoning",
    "industrial_agent": "agent",
}

DIFFICULTY_TO_LABEL = {
    1: "easy",
    2: "easy",
    3: "medium",
    4: "hard",
    5: "expert",
}


def iter_problem_files() -> list[Path]:
    return sorted(p for p in DATA_ROOT.rglob("*.yaml") if p.name != "index.yaml")


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} top-level YAML value must be a mapping")
    return data


def unique_strings(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not isinstance(value, str):
            continue
        item = value.strip()
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def rubric_to_string(data: dict[str, Any]) -> str:
    public_rubric = {
        "evaluation_rubric": data.get("evaluation_rubric", {}),
        "score_cap_rules": data.get("score_cap_rules", []),
        "numeric_checks": data.get("numeric_checks", []),
        "generic_answer_penalty": data.get("generic_answer_penalty", {}),
        "structured_output_requirements": data.get("structured_output_requirements", {}),
        "disallowed_answers": data.get("disallowed_answers", []),
    }
    return yaml.safe_dump(public_rubric, allow_unicode=True, sort_keys=False, width=120).strip()


def infer_task_type(data: dict[str, Any]) -> str:
    if data.get("choices"):
        return "multiple_choice"
    if data.get("numeric_checks"):
        return "numeric_reasoning"
    structured = data.get("structured_output_requirements")
    if isinstance(structured, dict) and structured.get("required") is True:
        return "structured_reasoning"
    if data.get("difficulty") in {4, 5}:
        return "case_analysis"
    return "short_answer"


def convert_record(data: dict[str, Any]) -> dict[str, Any]:
    layer = data.get("layer", "")
    category = LAYER_TO_CATEGORY.get(str(layer), str(layer))
    difficulty = data.get("difficulty")
    expected_capabilities = unique_strings(
        list(data.get("expected_skills", []) or [])
        + [data.get("primary_skill", "")]
        + list(data.get("secondary_skills", []) or [])
    )
    tags = unique_strings(
        [
            "manufacturing",
            category,
            data.get("category", ""),
            data.get("domain", ""),
            data.get("subdomain", ""),
            data.get("primary_skill", ""),
        ]
    )

    record = {
        "id": str(data.get("id", "")),
        "version": VERSION,
        "domain": DOMAIN,
        "category": category,
        "sub_category": str(data.get("category", "")),
        "task_type": infer_task_type(data),
        "question": str(data.get("question", "")),
        "context": str(data.get("scenario", "")),
        "choices": list(data.get("choices", []) or []),
        "answer": str(data.get("reference_answer", "")),
        "rubric": rubric_to_string(data),
        "expected_capabilities": expected_capabilities,
        "difficulty": DIFFICULTY_TO_LABEL.get(difficulty, ""),
        "tags": tags,
        "source": SOURCE,
        "public": True,
        "requires_external_knowledge": False,
        "notes": "",
    }
    return {key: record[key] for key in SCHEMA_KEYS}


def validate_record_shape(record: dict[str, Any], source: Path) -> None:
    keys = list(record.keys())
    if keys != SCHEMA_KEYS:
        raise ValueError(f"{source}: schema keys do not match v2 schema")
    if record["task_type"] not in {
        "short_answer",
        "multiple_choice",
        "structured_reasoning",
        "case_analysis",
        "numeric_reasoning",
    }:
        raise ValueError(f"{source}: invalid task_type {record['task_type']!r}")
    if record["difficulty"] not in {"easy", "medium", "hard", "expert"}:
        raise ValueError(f"{source}: invalid difficulty {record['difficulty']!r}")


def main() -> int:
    records: list[dict[str, Any]] = []
    for path in iter_problem_files():
        record = convert_record(load_yaml(path))
        validate_record_shape(record, path)
        records.append(record)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")

    print(f"Exported {len(records)} records to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
