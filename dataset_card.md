---
pretty_name: Industrial Agent Benchmark
language:
  - ja
  - en
license: apache-2.0
task_categories:
  - question-answering
  - text-generation
tags:
  - manufacturing
  - industrial-ai
  - agents
  - evaluation
  - benchmark
size_categories:
  - n<1K
---

# Industrial Agent Benchmark v2.0.0

## Overview

Industrial Agent Benchmark is a public benchmark dataset for evaluating industrial and manufacturing agent capabilities. Version 2.0.0 packages the public benchmark questions as Hugging Face-compatible JSONL while keeping evaluation scripts and generated outputs outside the dataset artifact.

The dataset is intended to be loaded as:

```python
from datasets import load_dataset

dataset = load_dataset(
    "masahirosakae/industrial-agent-benchmark",
    split="test",
)

item = dataset[0]
```

Until the hosted dataset is published, the repository supports a local JSONL export workflow.

## Motivation

Industrial agent systems need evaluation tasks that reflect manufacturing constraints, quality gates, human approval boundaries, structured reasoning, risk tradeoffs, and data integrity requirements. This dataset provides synthetic but domain-oriented benchmark questions for developing and testing such evaluation workflows.

The v2.0.0 publication goal is to separate public benchmark data from non-public local run artifacts:

- Hugging Face hosts the public dataset.
- GitHub hosts scripts, documentation, and validation tools.
- Local evaluation outputs remain local and are not committed.
- Leaderboard infrastructure is deferred to later work.

## Dataset Structure

Each record is a single benchmark question with public reference material and a public rubric. Records do not contain generated model answers or model-specific evaluation results.

Primary files:

```text
data/v2/test.jsonl
docs/dataset_schema_v2.md
docs/dataset_export_v2.md
```

## Splits

| Split | Status | Description |
|---|---|---|
| `test` | Public | Public benchmark questions. |
| `dev` | Planned | Small public examples for tool and evaluation debugging. |
| `private` | Reserved | Reserved name only; not published in GitHub. |

The v2.0.0 prototype currently exports the public `test` split.

## Schema

Every record uses the same stable keys:

```json
{
  "id": "IA-HILB-001",
  "version": "2.0.0",
  "domain": "manufacturing",
  "category": "agent",
  "sub_category": "hil_boundary",
  "task_type": "short_answer",
  "question": "...",
  "context": "...",
  "choices": [],
  "answer": "...",
  "rubric": "...",
  "expected_capabilities": [
    "manufacturing_reasoning",
    "risk_identification",
    "human_in_the_loop_judgment"
  ],
  "difficulty": "medium",
  "tags": [
    "quality",
    "manufacturing",
    "human-in-the-loop"
  ],
  "source": "synthetic",
  "public": true,
  "requires_external_knowledge": false,
  "notes": ""
}
```

Required fields:

- `id`
- `version`
- `domain`
- `category`
- `sub_category`
- `task_type`
- `question`
- `answer`
- `rubric`
- `difficulty`
- `tags`

Optional but schema-stable fields:

- `context`
- `choices`
- `expected_capabilities`
- `source`
- `public`
- `requires_external_knowledge`
- `notes`

The `answer` field is a public reference answer, not a model output.

## Limitations

- The dataset is synthetic and should not be treated as operational manufacturing advice.
- Public reference answers and rubrics are included for evaluation development.
- The v2.0.0 dataset does not include generated answers, judge outputs, benchmark run artifacts, or per-run score files.
- The initial rule-based judge pipeline is a deterministic format/pipeline placeholder, not a final leaderboard scorer.
- Hosted Hugging Face loading is planned; local JSONL export is the current repository workflow until publication.

## Citation

If you use this dataset, cite the repository and version:

```bibtex
@misc{industrial_agent_benchmark_v2,
  title = {Industrial Agent Benchmark v2.0.0},
  author = {Sakae, Masahiro},
  year = {2026},
  howpublished = {\url{https://github.com/masahirosakae/industrial-agent-benchmark}},
  note = {Public benchmark dataset for industrial and manufacturing agent evaluation}
}
```

## Versioning

Version 2.0.0 is the active dataset architecture line. Version 1.1.0 is frozen as a pre-release benchmark snapshot.

Versioned artifacts should document:

- dataset version
- schema version
- split names
- evaluator compatibility
- known limitations

Generated local evaluation outputs are not part of the published dataset.
