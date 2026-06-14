# Industrial Agent Benchmark

Industrial Agent Benchmark is a public benchmark for evaluating industrial and manufacturing agent capabilities. It is designed for tasks where factual manufacturing knowledge, multi-step operational reasoning, and safe agent behavior all matter.

The default Japanese README is available at [README.md](README.md).

## Dataset Overview

v2.0.0 is the Stable English Release. It contains 180 public benchmark questions and exports to Hugging Face-compatible JSONL.

| Layer | Count | Focus |
|---|---:|---|
| Industrial Knowledge | 60 | Manufacturing operations, quality, maintenance, change control, and procedural knowledge |
| Industrial Reasoning | 60 | Root-cause analysis, FMEA, CAPA, risk tradeoffs, data integrity, and numeric capacity planning |
| Industrial Agent | 60 | Workflow design, tool selection, human-in-the-loop boundaries, safety, structured decisions, and tool trajectories |
| Total | 180 |  |

Local dataset artifact:

```text
data/v2/test.jsonl
```

Dataset card:

```text
dataset_card.md
```

The dataset is intended to be easy to publish or load through Hugging Face Datasets while keeping evaluation outputs separate from the dataset artifact.

## Quick Start

### Requirements

- Python 3.10+
- PyYAML

```bash
pip install pyyaml
```

### Validate the YAML benchmark files

```bash
python scripts/validate_dataset.py
```

Expected output:

```text
Checked: 180 problem files
Errors: 0
Warnings:0
```

### Export and validate the HF-compatible JSONL

```bash
python scripts/export_hf_dataset_v2.py
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

### Load with Hugging Face Datasets

```bash
python examples/load_dataset_v2.py
```

## Repository Layout

```text
industrial-agent-benchmark/
  README.md
  README_EN.md
  dataset_card.md
  data/
    v2/
      test.jsonl
  benchmark_data/
    index.yaml
    index.csv
    knowledge/
    reasoning/
    agent/
  docs/
  examples/
  eval/
  scripts/
```

## Evaluation Architecture

The benchmark is organized around three evaluation layers.

| Layer | Judge direction | Notes |
|---|---|---|
| Industrial Knowledge | Deterministic Judge | Clear expected points, keywords, and structured reference answers |
| Industrial Reasoning | Rubric Judge plus numeric checks | Multi-step reasoning with evidence, constraints, feasibility, and calculation checks |
| Industrial Agent | Executable Judge | Safe workflow behavior, gate checks, tool/action boundaries, escalation, and audit trail requirements |

The public repository includes dataset validation, JSONL export, schema documentation, and simple local evaluation utilities. It does not include raw model answers, provider-specific outputs, private evaluation results, or leaderboard data.

## Hugging Face Dataset Path

The release artifact is prepared around:

- [dataset_card.md](dataset_card.md)
- [data/v2/test.jsonl](data/v2/test.jsonl)
- [docs/dataset_schema_v2.md](docs/dataset_schema_v2.md)
- [docs/dataset_export_v2.md](docs/dataset_export_v2.md)

When published to Hugging Face Hub, these files are the intended entry points for dataset loading and documentation.

## Citation

If you use Industrial Agent Benchmark in research, evaluation, or public reporting, cite the repository and release version.

```text
Industrial Agent Benchmark v2.0.0.
https://github.com/masahirosakae/industrial-agent-benchmark
```

A formal citation entry may be added after publication metadata is finalized.

## Contributing

Contributions should preserve the benchmark's public-release constraints:

- keep benchmark items manufacturing-domain relevant and public safe
- do not include private company data, customer data, proprietary process data, or provider-specific model results
- keep generated answers and evaluation outputs out of git
- update dataset validation/export files only through the documented scripts
- keep v2.0.0 as an English dataset release; multilingual English/Japanese design is planned for v2.1.0

Before proposing dataset changes, run:

```bash
python scripts/validate_dataset.py
python scripts/export_hf_dataset_v2.py
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

## License

Code: Apache License 2.0. See [LICENSE](LICENSE).

Dataset: see [LICENSE_DATASET.md](LICENSE_DATASET.md).
