# Industrial Agent Benchmark v1.0 Release Notes

Release: v1.0  
Date: 2026-06-06

---

## 1. Benchmark Overview

Industrial Agent Benchmark v1.0 is a benchmark dataset for evaluating AI agents in manufacturing scenarios.

The benchmark is designed to evaluate practical manufacturing capabilities rather than simple terminology recall. It focuses on:

1. Manufacturing domain knowledge
2. Manufacturing reasoning
3. Manufacturing problem solving
4. Industrial agent design

This release completes the v1.0 benchmark dataset and evaluation methodology.

---

## 2. Dataset Size

| Layer | Count |
|---|---:|
| Industrial Knowledge | 40 |
| Industrial Reasoning | 30 |
| Industrial Agent | 20 |
| **Total** | **90** |

Each benchmark item is stored as one YAML file under `benchmark_data/`.

---

## 3. Layer Structure

### Layer 1: Industrial Knowledge

Categories:

- Order
- Production Planning
- Procurement
- Manufacturing Preparation
- Manufacturing Execution
- Quality
- Shipping
- Improvement

Each category contains 5 items.

### Layer 2: Industrial Reasoning

Categories:

- FTA
- 5Why
- FMEA
- CAPA
- Quality Improvement
- Abnormality Analysis

Each category contains 5 items.

### Layer 3: Industrial Agent

Categories:

- Workflow Design
- Agent Design
- MCP
- Tool Selection
- Human in the Loop
- Multi Agent Coordination

Layer 3 contains 20 items.

---

## 4. Difficulty Distribution

| Difficulty | Definition | Count |
|---:|---|---:|
| 1 | Basic Operator | 0 |
| 2 | Junior Engineer | 0 |
| 3 | Mid-level Engineer | 34 |
| 4 | Senior Expert | 44 |
| 5 | Factory Director / Chief Engineer | 12 |

v1.0 focuses on difficulty levels 3 to 5. Future releases may add difficulty 1 to 2 items for score calibration.

---

## 5. Quality Review Summary

The v1.0 dataset review confirmed:

- All 90 items follow the benchmark schema.
- All items include `reference_answer`.
- All items include `evaluation_rubric`.
- All items include `critical_failures`.
- No pure definition-only or memorization-only items were identified.
- No exact duplicate items were identified.
- Several checklist-prone items were strengthened with additional constraints.

Examples of added constraints:

- numeric constraints
- cost constraints
- delivery constraints
- conflicting data
- trade-off conditions

---

## 6. Evaluation Assets

The following assets are included:

| File | Purpose |
|---|---|
| `evaluation_set_v1.yaml` | Representative 15-item evaluation subset |
| `judge_template.md` | Judging prompt template |
| `results_template.csv` | Empty result recording template |
| `docs/benchmark_release_notes_v1.0.md` | Release notes |

### Evaluation Subset

`evaluation_set_v1.yaml` contains 15 representative items.

| Layer | Count |
|---|---:|
| Knowledge | 5 |
| Reasoning | 5 |
| Agent | 5 |
| **Total** | **15** |

Selection criteria:

- domain balance
- difficulty balance
- skill balance
- HLE-style task fit
- rubric clarity

---

## 7. Known Limitations

1. Difficulty 1 to 2 items are not included in v1.0.
2. `general_manufacturing` is the largest domain.
3. `assembly` is the largest subdomain.
4. The current release focuses on dataset and methodology, not a live agent execution harness.
5. Some agent tasks evaluate design quality rather than runtime execution traces.

---

## 8. Future Work

Future releases may include:

- difficulty 1 to 2 calibration items
- additional medical device, heavy machinery, semiconductor, food, and chemical manufacturing scenarios
- stronger structured output validation
- transaction-safe tool-use scenarios
- traceability and measurement-system-analysis tasks
- live agent execution harnesses

---

## 9. Validation

Validate the dataset with:

```bash
python scripts/validate_dataset.py
```

Expected result:

```text
Checked: 90 problem files
Errors:  0
Warnings:0
```

---

## 10. Release Status

Industrial Agent Benchmark v1.0 is ready for use as an open benchmark dataset and evaluation methodology for manufacturing-domain AI agent research.

