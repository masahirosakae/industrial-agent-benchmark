#!/usr/bin/env python3
"""generate_dataset.py

Industrial Agent Benchmark v1.0 helper script.

Canonical dataset source is the set of individual YAML files under
benchmark_data/. This script regenerates benchmark_data/index.yaml and
benchmark_data/index.csv from those YAML files. It does not overwrite
problem YAML files.
"""
from __future__ import annotations
import csv
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "benchmark_data"
INDEX_YAML = DATA_ROOT / "index.yaml"
INDEX_CSV = DATA_ROOT / "index.csv"

FIELDS = [
    "id", "layer", "category", "domain", "subdomain", "difficulty",
    "estimated_time_min", "primary_skill", "file_path",
]

def iter_problem_files():
    for p in sorted(DATA_ROOT.rglob("*.yaml")):
        if p.name == "index.yaml":
            continue
        yield p

def main():
    rows = []
    by_layer = {}
    for path in iter_problem_files():
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT).as_posix()
        row = {
            "id": data["id"],
            "layer": data["layer"],
            "category": data["category"],
            "domain": data["domain"],
            "subdomain": data["subdomain"],
            "difficulty": data["difficulty"],
            "estimated_time_min": data["estimated_time_min"],
            "primary_skill": data["primary_skill"],
            "file_path": rel,
        }
        rows.append(row)
        by_layer[row["layer"]] = by_layer.get(row["layer"], 0) + 1

    rows.sort(key=lambda r: r["id"])
    INDEX_YAML.write_text(
        yaml.dump({
            "version": "1.0",
            "total_count": len(rows),
            "by_layer": by_layer,
            "items": rows,
        }, sort_keys=False, allow_unicode=True, width=10000),
        encoding="utf-8",
    )

    with INDEX_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Regenerated {INDEX_YAML} and {INDEX_CSV} from {len(rows)} problem files.")

if __name__ == "__main__":
    main()
