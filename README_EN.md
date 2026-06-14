# Industrial Agent Benchmark

Industrial Agent Benchmark is a public benchmark for evaluating Industrial AI systems, Manufacturing AI assistants, and Industrial Agents.

The canonical language of Industrial Agent Benchmark is **Japanese**. English should be treated as a future translated or derivative distribution, not as the source of truth.

Japanese README: [README.md](README.md)

## Dataset Overview

**Current release: v2.2.0 Japanese Canonical Normalization**

v2.2.0 completed the migration of previously English-only benchmark tasks into Japanese canonical form while preserving the dataset size and validation pipeline.

- Total: 180 tasks
- Knowledge: 60
- Reasoning: 60
- Agent: 60
- English-only tasks: 45 -> 0
- HF-compatible JSONL: `data/v2/test.jsonl`
- Validation/export pipeline: preserved

Some compatibility fields inside `data/v2/test.jsonl` may retain historical schema values. The public release state is v2.2.0.

| Layer | Count | Focus |
|---|---:|---|
| Industrial Knowledge | 60 | Manufacturing knowledge, procedures, quality, maintenance, and change control |
| Industrial Reasoning | 60 | Root-cause analysis, FMEA, CAPA, risk tradeoffs, data integrity, and numeric capacity planning |
| Industrial Agent | 60 | Workflow design, tool selection, human approval boundaries, safety, structured decisions, and auditability |
| Total | 180 |  |

## Language Policy

v2.2.0 establishes Japanese as the canonical language for benchmark tasks.

- Japanese records are the source of truth.
- English is planned as a translated or derivative distribution.
- English-only task records have been migrated to Japanese canonical form.
- Machine-readable schema keys, enum-like final states, JSON field names, and accepted technical abbreviations may remain in English where needed for evaluation compatibility.

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

### Load locally

```bash
python examples/load_dataset_v2.py
```

## Hugging Face Dataset

```text
https://huggingface.co/datasets/MSakae/industrial-agent-benchmark
```

Primary dataset file:

```text
data/v2/test.jsonl
```

## Evaluation Architecture

| Layer | Judge direction | Notes |
|---|---|---|
| Industrial Knowledge | Deterministic Judge | Expected points, keywords, and structured reference answers |
| Industrial Reasoning | Rubric Judge plus numeric checks | Evidence, constraints, feasibility, and calculation checks |
| Industrial Agent | Executable Judge | Safe workflow behavior, gate checks, action boundaries, escalation, and audit trails |

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
    knowledge/
    reasoning/
    agent/
  docs/
  examples/
  eval/
  scripts/
```

## Citation

If you use Industrial Agent Benchmark in research, evaluation, or public reporting, cite the repository and release version.

```text
Industrial Agent Benchmark v2.2.0.
https://github.com/masahirosakae/industrial-agent-benchmark
```

## Contributing

Contributions should preserve the benchmark's public-release constraints:

- keep benchmark items manufacturing-domain relevant and public safe
- treat Japanese as the canonical language
- do not include private company data, customer data, proprietary process data, or provider-specific model results
- keep generated answers and evaluation outputs out of git
- update derived JSONL only through the documented export script

Before proposing dataset changes, run:

```bash
python scripts/validate_dataset.py
python scripts/export_hf_dataset_v2.py
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

## License

Code: Apache License 2.0. See [LICENSE](LICENSE).

Dataset: see [LICENSE_DATASET.md](LICENSE_DATASET.md).
