#!/usr/bin/env python3
"""validate_dataset.py
Industrial Agent Benchmark v1.0 dataset validator.

Checks (per docs/benchmark_spec.md):
- required fields exist
- ids are globally unique
- difficulty in 1..5
- evaluation_rubric has must_have / nice_to_have / critical_failures (non-empty)
- file_path matches id and category
- enum values are valid
- primary_skill / secondary_skills consistent with expected_skills
- index files are consistent with on-disk YAMLs
"""
from __future__ import annotations
import sys
import csv
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "benchmark_data"

REQUIRED_FIELDS = [
    "id","layer","category","domain","subdomain","difficulty","estimated_time_min",
    "title","scenario","question","expected_skills","primary_skill","secondary_skills",
    "reference_answer","evaluation_rubric","reasoning_trace_required",
]

VALID_LAYERS = {"industrial_knowledge","industrial_reasoning","industrial_agent"}
LAYER_DIR = {
    "industrial_knowledge": "knowledge",
    "industrial_reasoning": "reasoning",
    "industrial_agent": "agent",
}
VALID_CATEGORIES = {
    "industrial_knowledge": {
        "order","production_planning","procurement","manufacturing_preparation",
        "manufacturing_execution","quality","shipping","improvement",
    },
    "industrial_reasoning": {
        "fta","5why","fmea","capa","quality_improvement","abnormality_analysis",
    },
    "industrial_agent": {
        "workflow_design","agent_design","mcp","tool_selection",
        "human_in_the_loop","multi_agent_coordination",
    },
}
VALID_DOMAINS = {
    "automotive","electronics","medical_device","heavy_machinery","general_manufacturing",
}
VALID_SUBDOMAINS = {
    "assembly","smt","molding","machining","welding","coating","inspection",
    "logistics","procurement","production_control","quality_assurance",
    "maintenance","supply_chain_management","process_engineering",
}

ID_PREFIX = {
    "industrial_knowledge": "IK",
    "industrial_reasoning": "IR",
    "industrial_agent": "IA",
}
CATEGORY_PREFIX = {
    "order":"ORDER","production_planning":"PP","procurement":"PROC",
    "manufacturing_preparation":"MPREP","manufacturing_execution":"MEXEC",
    "quality":"QUAL","shipping":"SHIP","improvement":"IMPR",
    "fta":"FTA","5why":"5WHY","fmea":"FMEA","capa":"CAPA",
    "quality_improvement":"QI","abnormality_analysis":"AA",
    "workflow_design":"WD","agent_design":"AD","mcp":"MCP",
    "tool_selection":"TS","human_in_the_loop":"HIL",
    "multi_agent_coordination":"MAC",
}

class Result:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checked = 0
    def err(self, ctx, msg): self.errors.append(f"[{ctx}] {msg}")
    def warn(self, ctx, msg): self.warnings.append(f"[{ctx}] {msg}")

def validate_problem(path: Path, data: dict, seen_ids: set, result: Result):
    pid = data.get("id", "<unknown>")
    ctx = f"{path.relative_to(ROOT)}"

    # Required fields
    for f in REQUIRED_FIELDS:
        if f not in data:
            result.err(ctx, f"missing required field: {f}")
            return

    # id uniqueness
    if pid in seen_ids:
        result.err(ctx, f"duplicate id: {pid}")
    seen_ids.add(pid)

    # layer
    layer = data["layer"]
    if layer not in VALID_LAYERS:
        result.err(ctx, f"invalid layer: {layer}")
        return

    # category
    cat = data["category"]
    if cat not in VALID_CATEGORIES[layer]:
        result.err(ctx, f"invalid category for {layer}: {cat}")

    # domain / subdomain
    if data["domain"] not in VALID_DOMAINS:
        result.err(ctx, f"invalid domain: {data['domain']}")
    if data["subdomain"] not in VALID_SUBDOMAINS:
        result.err(ctx, f"invalid subdomain: {data['subdomain']}")

    # difficulty
    diff = data["difficulty"]
    if not isinstance(diff, int) or diff < 1 or diff > 5:
        result.err(ctx, f"difficulty must be int 1..5, got {diff!r}")

    # estimated_time_min
    et = data["estimated_time_min"]
    if not isinstance(et, int) or et <= 0:
        result.err(ctx, f"estimated_time_min must be positive int, got {et!r}")

    # id prefix matches layer/category
    expected_prefix = f"{ID_PREFIX[layer]}-{CATEGORY_PREFIX[cat]}-"
    if not pid.startswith(expected_prefix):
        result.err(ctx, f"id {pid!r} does not start with {expected_prefix!r}")

    # file_path matches id
    expected_path = DATA_ROOT / LAYER_DIR[layer] / cat / f"{pid}.yaml"
    if path.resolve() != expected_path.resolve():
        result.err(ctx, f"file path does not match id; expected {expected_path}")

    # text fields non-empty
    for f in ("title","scenario","question","reference_answer"):
        v = data.get(f)
        if not isinstance(v, str) or not v.strip():
            result.err(ctx, f"{f} must be non-empty string")

    # expected_skills list non-empty
    es = data["expected_skills"]
    if not isinstance(es, list) or not es:
        result.err(ctx, "expected_skills must be non-empty list")
        es = []
    if not all(isinstance(x, str) for x in es):
        result.err(ctx, "expected_skills must be list of strings")

    # primary_skill must be in expected_skills
    ps = data["primary_skill"]
    if ps not in es:
        result.err(ctx, f"primary_skill {ps!r} not in expected_skills")

    # secondary_skills must be subset of expected_skills and exclude primary
    ss = data["secondary_skills"]
    if not isinstance(ss, list):
        result.err(ctx, "secondary_skills must be list")
        ss = []
    for s in ss:
        if s not in es:
            result.err(ctx, f"secondary_skill {s!r} not in expected_skills")
        if s == ps:
            result.err(ctx, f"primary_skill {ps!r} duplicated in secondary_skills")

    # evaluation_rubric
    rub = data["evaluation_rubric"]
    if not isinstance(rub, dict):
        result.err(ctx, "evaluation_rubric must be dict")
    else:
        for k in ("must_have","nice_to_have","critical_failures"):
            v = rub.get(k)
            if not isinstance(v, list):
                result.err(ctx, f"evaluation_rubric.{k} must be list")
            elif not v:
                # critical_failures and must_have should not be empty
                if k in ("must_have","critical_failures"):
                    result.err(ctx, f"evaluation_rubric.{k} must be non-empty")
                else:
                    result.warn(ctx, f"evaluation_rubric.{k} is empty")
            else:
                if not all(isinstance(x, str) and x.strip() for x in v):
                    result.err(ctx, f"evaluation_rubric.{k} must contain non-empty strings")

    # reasoning_trace_required
    rt = data["reasoning_trace_required"]
    if not isinstance(rt, bool):
        result.err(ctx, f"reasoning_trace_required must be bool, got {rt!r}")

def validate_index(yaml_path: Path, csv_path: Path, on_disk_ids: set, result: Result):
    if not yaml_path.exists():
        result.err("index.yaml", "missing")
    else:
        with yaml_path.open("r", encoding="utf-8") as f:
            idx = yaml.safe_load(f)
        items = idx.get("items", [])
        idx_ids = {it["id"] for it in items}
        missing = on_disk_ids - idx_ids
        extra = idx_ids - on_disk_ids
        if missing:
            result.err("index.yaml", f"missing ids: {sorted(missing)}")
        if extra:
            result.err("index.yaml", f"extra ids not on disk: {sorted(extra)}")
        if idx.get("total_count") != len(items):
            result.err("index.yaml", f"total_count {idx.get('total_count')} != items {len(items)}")

    if not csv_path.exists():
        result.err("index.csv", "missing")
    else:
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            csv_ids = {row["id"] for row in reader}
        missing = on_disk_ids - csv_ids
        extra = csv_ids - on_disk_ids
        if missing:
            result.err("index.csv", f"missing ids: {sorted(missing)}")
        if extra:
            result.err("index.csv", f"extra ids not on disk: {sorted(extra)}")

def main():
    result = Result()
    seen_ids = set()
    on_disk_ids = set()

    yaml_files = sorted(DATA_ROOT.rglob("*.yaml"))
    # exclude index.yaml
    yaml_files = [p for p in yaml_files if p.name != "index.yaml"]

    for path in yaml_files:
        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            result.err(str(path), f"yaml parse error: {e}")
            continue
        if not isinstance(data, dict):
            result.err(str(path), f"top-level must be dict, got {type(data).__name__}")
            continue
        validate_problem(path, data, seen_ids, result)
        result.checked += 1
        if "id" in data:
            on_disk_ids.add(data["id"])

    validate_index(DATA_ROOT / "index.yaml", DATA_ROOT / "index.csv", on_disk_ids, result)

    # Summary
    print(f"Checked: {result.checked} problem files")
    print(f"Errors:  {len(result.errors)}")
    print(f"Warnings:{len(result.warnings)}")
    for e in result.errors:
        print(f"  ERR  {e}")
    for w in result.warnings:
        print(f"  WARN {w}")

    sys.exit(1 if result.errors else 0)

if __name__ == "__main__":
    main()
