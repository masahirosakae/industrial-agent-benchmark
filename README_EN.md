# Industrial Agent Benchmark

This is the English public README for Industrial Agent Benchmark. v1.1.0 is frozen as a pre-release benchmark snapshot, and v2.0.0 is the current public release-candidate line.

## v2.0.0 Dataset Composition

The v2.0.0 release candidate contains 180 public benchmark questions:

| Layer | Count |
|---|---:|
| Industrial Knowledge | 60 |
| Industrial Reasoning | 60 |
| Industrial Agent | 60 |
| Total | 180 |

The dataset is exported as Hugging Face-compatible JSONL at `data/v2/test.jsonl`.

## Quick Start

### Requirements

- Python 3.10+
- PyYAML

```bash
pip install pyyaml
```

### Validate Dataset

```bash
python scripts/validate_dataset.py
```

Expected output:

```text
Checked: 180 problem files
Errors: 0
Warnings:0
```

### Inspect Questions

```bash
cat benchmark_data/knowledge/order/IK-ORDER-001.yaml
cat benchmark_data/agent/hil_boundary/IA-HILB-001.yaml
```

### Judge v2 Workflow

Judge v2 requires model answer files and is not runnable from a fresh clone without answers.

Expected answer layout:

```text
results_v2/<model_id>/answers/<question_id>.txt
```

`results_v2/` is intentionally excluded from the public repository.

To prepare judge inputs after generating your own answers:

```bash
python scripts/prepare_judge_inputs_v2.py <model_id>
```

Example:

```bash
python scripts/prepare_judge_inputs_v2.py my_model
```

Do not use a placeholder model ID unless matching answer files exist locally.

## v2.0.0 Dataset Export

v2.0.0 exports the public YAML benchmark questions from `benchmark_data/` to Hugging Face-compatible JSONL. The exported file follows the stable schema in `docs/dataset_schema_v2.md`.

Export the local JSONL dataset:

```bash
python scripts/export_hf_dataset_v2.py
```

Validate the exported dataset:

```bash
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

Load the local JSONL dataset with Hugging Face Datasets:

```bash
python examples/load_dataset_v2.py
```

Hugging Face hosted loading is planned for publication. The local JSONL export is the supported v2.0.0 release-candidate workflow and should produce 180 records.

## Public Artifact Policy

Do not commit raw model answers, model-specific results, judge outputs, private reports, provider/model-name mappings, API keys, `.env` files, tokens, or credentials.

Private or generated outputs such as `results_v2/`, `results/`, and `judgements/` are intentionally excluded from the public repository.
