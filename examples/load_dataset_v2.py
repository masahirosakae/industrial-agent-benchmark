#!/usr/bin/env python3
"""Load the v2.0.0 JSONL dataset with Hugging Face Datasets."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Avoid importing this repository's local datasets/ directory as a namespace
# package when the Hugging Face `datasets` dependency is not installed.
sys.path = [p for p in sys.path if p not in {"", str(ROOT)}]

try:
    from datasets import load_dataset
except ImportError as exc:
    raise SystemExit(
        "Hugging Face Datasets is required for this example. "
        "Install dependencies with: python -m pip install -r requirements.txt"
    ) from exc


def main() -> None:
    dataset = load_dataset(
        "json",
        data_files={"test": "data/v2/test.jsonl"},
        split="test",
    )
    item = dataset[0]
    print(item["id"])
    print(item["task_type"])
    print(item["difficulty"])


if __name__ == "__main__":
    main()
