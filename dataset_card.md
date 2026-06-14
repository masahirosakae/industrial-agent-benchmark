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
  - industrial-agent
  - agent-evaluation
  - llm-evaluation
  - benchmark
size_categories:
  - n<1K
---

# Industrial Agent Benchmark v2.2.0

## Overview

Industrial Agent Benchmark is a public benchmark dataset for evaluating Industrial AI systems, Manufacturing AI assistants, and Industrial Agents.

**v2.2.0 is the Japanese Canonical Normalization release.** Japanese is now the canonical language of the benchmark. English should be treated as a future translated or derivative distribution, not as the source of truth.

v2.2.0 preserves the 180-task dataset composition and validation/export pipeline while migrating previously English-only tasks to Japanese canonical form.

## v2.2.0 Release Note

- Japanese Canonical Normalization completed.
- Previously English-only tasks migrated to Japanese canonical form.
- English-only tasks: 45 -> 0.
- Total tasks retained: 180.
- Layer balance retained: Knowledge 60 / Reasoning 60 / Agent 60.
- HF-compatible JSONL workflow preserved.
- No generated answers, private results, or provider-specific evaluation outputs are included.

Note: some machine-readable schema keys, enum-like final states, numeric check names, JSON field names, and accepted technical abbreviations may remain in English for evaluation compatibility.

## Dataset Structure

Primary files:

```text
data/v2/test.jsonl
docs/dataset_schema_v2.md
docs/dataset_export_v2.md
```

Each record is a single benchmark task with public reference material and a public rubric. Records do not contain generated model answers or model-specific evaluation results.

## Dataset Summary

| Layer | Count | Focus |
|---|---:|---|
| Knowledge | 60 | Manufacturing facts, procedures, constraints, governance, and reference-answer correctness |
| Reasoning | 60 | Root-cause analysis, risk tradeoffs, data integrity, CAPA, FMEA, and numeric capacity planning |
| Agent | 60 | Workflow design, tool use, human approval boundaries, safety, structured decisions, and auditability |
| Total | 180 | Balanced public benchmark split |

Category distribution:

| Layer | Category | Count |
|---|---|---:|
| Knowledge | `change_control` | 10 |
| Knowledge | `maintenance_engineering` | 10 |
| Knowledge | `improvement`, `manufacturing_execution`, `manufacturing_preparation`, `order`, `procurement`, `production_planning`, `quality`, `shipping` | 5 each |
| Reasoning | `data_integrity`, `numeric_capacity_planning`, `risk_tradeoff` | 10 each |
| Reasoning | `5why`, `abnormality_analysis`, `capa`, `fmea`, `fta`, `quality_improvement` | 5 each |
| Agent | `human_in_the_loop` | 13 |
| Agent | `workflow_design` | 14 |
| Agent | `agent_safety`, `hil_boundary`, `structured_decision`, `tool_trajectory` | 5 each |
| Agent | `agent_design` | 4 |
| Agent | `mcp`, `multi_agent_coordination`, `tool_selection` | 3 each |

## Task Format

Items are prompt-style benchmark records. A model or agent receives `context` and `question`, then produces a text or structured answer. Public `answer` and `rubric` fields are included for evaluation development and reproducibility.

## Splits

| Split | Status | Description |
|---|---|---|
| `test` | Public | Public benchmark tasks |

The v2.2.0 release uses the public `test` split with 180 records.

## Schema

Every record uses stable keys:

```json
{
  "id": "IA-HILB-001",
  "version": "2.0.0",
  "domain": "manufacturing",
  "category": "agent",
  "sub_category": "hil_boundary",
  "task_type": "case_analysis",
  "question": "...",
  "context": "...",
  "choices": [],
  "answer": "...",
  "rubric": "...",
  "expected_capabilities": [],
  "difficulty": "hard",
  "tags": [],
  "source": "synthetic",
  "public": true,
  "requires_external_knowledge": false,
  "notes": ""
}
```

The `version` field is retained for schema compatibility with the existing v2 JSONL pipeline. The current public release state is v2.2.0.

## Intended Use

- Evaluate industrial and manufacturing agent capabilities.
- Develop public evaluation harnesses and judge workflows.
- Test handling of manufacturing constraints, approval boundaries, evidence traceability, and structured reasoning.
- Support local, reproducible benchmark experimentation without committing generated answers or run artifacts.

## Limitations

- The dataset is synthetic and should not be treated as operational manufacturing advice.
- The benchmark is not a certification benchmark.
- It does not cover all manufacturing domains, sectors, product types, or factory systems.
- English translation pairs are not yet the source of truth; English is planned as a derivative distribution.
- Machine-readable schema and evaluation compatibility fields may remain in English.

## Evaluation

The GitHub repository provides validation and evaluation scripts:

- `scripts/validate_dataset.py`
- `scripts/export_hf_dataset_v2.py`
- `scripts/validate_hf_dataset_v2.py`
- `eval/run_simple_eval.py`
- `eval/run_judge_eval.py`

Example validation:

```bash
python scripts/validate_dataset.py
python scripts/export_hf_dataset_v2.py
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

## Citation

If you use this dataset, cite the repository and release version:

```bibtex
@misc{sakae2026industrialagentbenchmark,
  title = {Industrial Agent Benchmark},
  author = {Masahiro Sakae},
  year = {2026},
  version = {2.2.0},
  url = {https://github.com/masahirosakae/industrial-agent-benchmark}
}
```

## License

Apache License 2.0. See the GitHub repository for full license files and dataset release notes.
