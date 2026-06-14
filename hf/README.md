---
language:
  - en
  - ja
license: apache-2.0
pretty_name: Industrial Agent Benchmark
task_categories:
  - question-answering
tags:
  - manufacturing
  - industrial-ai
  - industrial-agent
  - llm-evaluation
  - agent-evaluation
  - benchmark
size_categories:
  - n<1K
---

# Industrial Agent Benchmark

Industrial Agent Benchmark (IAB) is an open benchmark for evaluating Industrial AI systems, Manufacturing AI assistants, and Industrial Agents.

This Dataset Card describes the Hugging Face Dataset release for **Industrial Agent Benchmark v2.0.0 Stable Release**.

Repository:

```text
https://github.com/masahirosakae/industrial-agent-benchmark
```

Hugging Face Dataset Repository:

```text
https://huggingface.co/datasets/MSakae/industrial-agent-benchmark
```

## Dataset Description

Industrial Agent Benchmark evaluates whether AI systems can handle manufacturing-domain tasks across three layers:

- **Knowledge**: factual and procedural manufacturing knowledge
- **Reasoning**: multi-step industrial reasoning, risk analysis, root-cause analysis, and numeric planning
- **Agent**: workflow design, tool-use boundaries, human approval requirements, safe escalation, and auditability

v2.0.0 is the first stable public release and contains English and Japanese benchmark tasks. v2.0.1 corrects the dataset metadata and documentation to reflect this multilingual reality without changing the 180 examples or JSONL schema. Multilingual architecture and language-specific design are planned for v2.1.0.

## Dataset Statistics

| Split | Examples |
|---|---:|
| test | 180 |

| Layer | Examples |
|---|---:|
| Knowledge | 60 |
| Reasoning | 60 |
| Agent | 60 |
| Total | 180 |

Difficulty distribution in `data/v2/test.jsonl`:

| Difficulty | Examples |
|---|---:|
| easy | 4 |
| medium | 55 |
| hard | 91 |
| expert | 30 |

## Intended Use

This dataset is designed for:

- Manufacturing AI evaluation
- Industrial LLM evaluation
- Industrial Agent evaluation
- Research on domain-specific AI evaluation
- Comparing model behavior on industrial knowledge, reasoning, and agent-safety tasks

The benchmark is intended for research and evaluation. It is not a certification benchmark.

## Dataset Structure

v2.0.0 contains English and Japanese benchmark tasks organized into three layers:

- `knowledge`
- `reasoning`
- `agent`

The dataset is distributed as JSONL and uses a single `test` split.

## Data Files

Primary data file:

```text
data/v2/test.jsonl
```

The JSONL file is generated from the public YAML benchmark items in the GitHub repository.

## Data Fields

The following fields are present in `data/v2/test.jsonl`:

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable benchmark item ID. |
| `version` | string | Dataset item version, currently `2.0.0`. |
| `domain` | string | High-level domain label. |
| `category` | string | Benchmark layer category: `knowledge`, `reasoning`, or `agent`. |
| `sub_category` | string | More specific task category within the layer. |
| `task_type` | string | Task format label, such as case-analysis style tasks. |
| `question` | string | Main prompt or question to answer. |
| `context` | string | Scenario or supporting context for the task. |
| `choices` | list | Multiple-choice options when present; empty for open tasks. |
| `answer` | string | Reference answer. |
| `rubric` | string | Evaluation rubric or grading guidance. |
| `expected_capabilities` | list | Capabilities expected for the task. |
| `difficulty` | string | Difficulty label: `easy`, `medium`, `hard`, or `expert`. |
| `tags` | list | Search and grouping tags. |
| `source` | string | Source type. v2.0.0 items are synthetic benchmark tasks. |
| `public` | boolean | Whether the item is public. |
| `requires_external_knowledge` | boolean | Whether external knowledge is required. |
| `notes` | string | Optional notes. |

## Loading Example

Standard loading after publication:

```python
from datasets import load_dataset

dataset = load_dataset("MSakae/industrial-agent-benchmark")
print(dataset)
```

If you need to specify the data file manually:

```python
from datasets import load_dataset

dataset = load_dataset(
    "json",
    data_files={"test": "data/v2/test.jsonl"},
)
print(dataset)
```

## Evaluation

The GitHub repository provides validation and evaluation scripts:

- `scripts/validate_hf_dataset_v2.py`
- `eval/run_simple_eval.py`
- `eval/run_judge_eval.py`

The dataset card describes the benchmark data. Evaluation outputs, generated answers, model-specific results, private reports, and leaderboard artifacts are intentionally not included in the dataset release.

Example validation:

```bash
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

Simple local evaluation utilities are available in the GitHub repository for users who generate their own answer files.

## Limitations

- v2.0.0 contains English, Japanese, and mixed-language records.
- The benchmark is not a certification benchmark and should not be used as proof of operational safety or regulatory compliance.
- It does not cover all manufacturing domains, sectors, product types, or factory systems.
- The dataset uses synthetic benchmark tasks and does not include private company data, customer data, or proprietary process data.
- v2.1.0 is planned for multilingual English + Japanese design.

## License

Apache License 2.0.

See the GitHub repository for full license files and dataset release notes.

## Citation

```bibtex
@misc{sakae2026industrialagentbenchmark,
  title = {Industrial Agent Benchmark},
  author = {Masahiro Sakae},
  year = {2026},
  version = {2.0.0},
  url = {https://github.com/masahirosakae/industrial-agent-benchmark}
}
```
