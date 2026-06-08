# Hugging Face Dataset Plan

This document defines the v2.0.0 plan for publishing Industrial Agent Benchmark through Hugging Face Datasets.

## Objective

Make the benchmark loadable with a standard dataset workflow while keeping evaluation scripts and policy in GitHub.

Target user experience:

```python
from datasets import load_dataset

dataset = load_dataset("industrial-agent-benchmark", split="validation")
```

The final dataset identifier may change before publication.

## Dataset Contents

The public dataset should include benchmark questions and public metadata:

- question ID
- version
- layer
- category
- domain
- subdomain
- difficulty
- title
- scenario
- question
- expected skills
- public rubric fields
- public evaluator metadata needed for reproducibility

The dataset must not include:

- raw model answers
- private judge outputs
- local result directories
- model-specific reports
- provider or model-name mappings
- API keys or credentials

## Splits and Configs

Recommended initial split:

| Split | Purpose |
|---|---|
| `validation` | Public benchmark questions for local evaluation. |

Optional future configs:

| Config | Purpose |
|---|---|
| `v1_1_0_snapshot` | Frozen pre-release compatibility snapshot. |
| `v2_0_0` | Active v2.0.0 dataset format. |

## Schema Preservation

v2.0.0 should preserve the meaning of current benchmark fields while making the loaded dataset easier to consume. Complex rubric fields may remain structured objects rather than being flattened into lossy strings.

Schema changes should be documented in `docs/versioning_policy.md`.

## Repository Role

GitHub should contain:

- dataset validation scripts
- simple evaluation scripts
- schema documentation
- example loading code
- leaderboard and versioning policy

GitHub should not contain generated model outputs or private evaluation artifacts.

## Publication Checklist

- [ ] Dataset card written.
- [ ] Dataset loads with `datasets.load_dataset`.
- [ ] All public examples use non-private data.
- [ ] No raw model answers are included.
- [ ] No private result directories are included.
- [ ] Dataset version matches repository documentation.
- [ ] Simple evaluation docs reference the dataset loading path.
