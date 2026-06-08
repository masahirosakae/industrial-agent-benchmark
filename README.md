# Industrial Agent Benchmark

Industrial Agent Benchmark is a public benchmark project for evaluating industrial and manufacturing agent capabilities. It covers industrial knowledge, industrial reasoning, and industrial agent behavior across practical manufacturing scenarios.

## Current Status

| Version | Status | Summary |
|---|---|---|
| v1.0 | Public baseline | Initial 90-problem benchmark and judge methodology. |
| v1.1.0 | Frozen pre-release snapshot | 140 public problem files, `evaluation_set_v2`, and Judge v2 materials. No further evaluation-result cleanup is planned on this line. |
| v2.0.0 | Active development | New architecture line targeting an HLE-style public workflow. |

v1.1.0 is frozen as a pre-release benchmark snapshot. The v1.1.0 dataset and evaluation materials remain available for inspection and compatibility work, but active development has moved to v2.0.0.

v2.0.0 aims to follow an HLE-style workflow:

- dataset loaded through Hugging Face Datasets
- GitHub repository provides evaluation scripts and documentation
- simple local evaluation first
- public leaderboard later
- no private model evaluation artifacts committed

The public repository does not include raw model answers, model-specific evaluation outputs, private reports, API keys, provider credentials, or unpublished model-evaluation artifacts.

## 1. Benchmark Scope

The benchmark is organized into three layers:

| Layer | Description |
|---|---|
| Industrial Knowledge | Domain knowledge for order handling, production planning, procurement, manufacturing, quality, shipping, improvement, and maintenance engineering. |
| Industrial Reasoning | Root-cause analysis, FMEA, CAPA, quality improvement, abnormality analysis, risk tradeoffs, and data integrity. |
| Industrial Agent | Workflow design, tool selection, MCP-style behavior, human-in-the-loop boundaries, agent safety, structured decisions, and tool trajectories. |

## 2. Repository Layout

```text
industrial-agent-benchmark/
  README.md
  README_EN.md
  benchmark_data/
    index.yaml
    index.csv
    knowledge/
    reasoning/
    agent/
  docs/
  evaluation_set_v1.yaml
  evaluation_set_v2.yaml
  judge_template.md
  judge_template_v2.md
  scripts/
    generate_dataset.py
    validate_dataset.py
    prepare_judge_inputs_v2.py
```

Private or generated outputs are intentionally excluded:

- `results_v2/`
- `results/`
- `judgements/`
- raw model answers
- judge outputs
- model-specific evaluation results
- private notes and unpublished reports
- API keys, `.env` files, tokens, and provider credentials

## 3. v1.1.0 Snapshot

The frozen v1.1.0 snapshot includes:

- 140 benchmark problem files under `benchmark_data/`
- `evaluation_set_v1.yaml`
- `evaluation_set_v2.yaml`
- Judge templates for external evaluation workflows
- dataset generation and validation scripts

`evaluation_set_v2.yaml` contains 30 questions:

- Knowledge: 10
- Reasoning: 10
- Agent: 10

Judge v2 supports:

- `score_cap_rules`
- `numeric_checks`
- `generic_answer_penalty`
- `structured_output_requirements`
- `disallowed_answers`
- `critical_failures`

## 4. Quick Start

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
Checked: 140 problem files
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

## 5. v2.0.0 Dataset Export

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

Hugging Face hosted loading is planned, but it is not required until the dataset is published. For now, the local JSONL export is the supported v2.0.0 prototype workflow.

## 6. v2.0.0 Planning Documents

| Document | Purpose |
|---|---|
| `docs/v1_1_0_freeze_note.md` | Freezes v1.1.0 as a pre-release snapshot. |
| `docs/v2_0_0_architecture.md` | Defines the active v2.0.0 architecture direction. |
| `docs/huggingface_dataset_plan.md` | Plans Hugging Face dataset packaging and loading. |
| `docs/dataset_schema_v2.md` | Defines the stable v2.0.0 dataset schema. |
| `docs/dataset_export_v2.md` | Documents the local v2.0.0 JSONL export workflow. |
| `docs/simple_evaluation_plan.md` | Defines the first simple public evaluation workflow. |
| `docs/leaderboard_policy.md` | Defines future leaderboard governance. |
| `docs/versioning_policy.md` | Defines versioning and compatibility policy. |

Additional public documentation:

| Document | Purpose |
|---|---|
| `docs/benchmark_card.md` | Benchmark card. |
| `docs/benchmark_spec.md` | Problem schema and benchmark specification. |
| `docs/evaluation_methodology.md` | Evaluation methodology and judge concepts. |
| `docs/difficulty_definition.md` | Difficulty definition. |
| `docs/v1.1_release_notes.md` | v1.1.0 pre-release notes. |
| `docs/public_repository_audit.md` | Public repository audit and release checklist. |

## 7. Public Artifact Policy

The repository is intended to be usable from a fresh public clone. Public users should be able to validate the dataset and inspect benchmark problems without any private answer or result directories.

Evaluation scripts that consume answers require locally generated answer files. They should fail clearly when those files are absent.

Do not commit:

- raw model answers
- `results_v2/`
- `results/`
- judge inputs or judge outputs
- model-specific evaluation results
- unpublished reports
- provider/model-name mappings
- API keys or secrets

## 8. License

Apache License 2.0. See `LICENSE`.
