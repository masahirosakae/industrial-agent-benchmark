# Benchmark Card: Industrial Agent Benchmark v1.0

## Overview

Industrial Agent Benchmark is an open benchmark dataset for evaluating AI agent capabilities in manufacturing workflows.

The benchmark focuses on practical manufacturing scenarios that require domain knowledge, reasoning, risk assessment, and agent-oriented workflow design.

## Intended Use

This benchmark is intended for:

- Evaluating manufacturing-domain reasoning
- Testing structured problem solving under operational constraints
- Assessing workflow and agent design for industrial use cases
- Comparing benchmark runs within a controlled evaluation setup

It is not intended to replace expert review for safety-critical, legal, regulatory, or production release decisions.

## Dataset Structure

The v1.0 dataset contains 90 YAML benchmark items.

| Layer | Count | Scope |
|---|---:|---|
| Industrial Knowledge | 40 | Manufacturing operations and process knowledge |
| Industrial Reasoning | 30 | Root cause analysis, risk analysis, and improvement reasoning |
| Industrial Agent | 20 | Workflow, tool, coordination, and human approval design |

## Evaluation Design

Each item includes:

- `scenario`
- `question`
- `reference_answer`
- `evaluation_rubric.must_have`
- `evaluation_rubric.nice_to_have`
- `evaluation_rubric.critical_failures`

During answer generation, only the scenario and question should be provided to the evaluated system. Reference answers and rubrics are intended for judging only.

## Scoring

The recommended scoring method uses a judging process that checks:

- critical failures
- required rubric coverage
- optional rubric coverage
- reasoning quality
- manufacturing feasibility

See `docs/evaluation_methodology.md` for details.

## Known Limitations

- v1.0 focuses on difficulty levels 3 to 5.
- Some categories are more represented than others.
- Current evaluation is text-based and does not yet include a live execution harness.
- Safety-critical outputs should always be reviewed by qualified human experts.

## License

Industrial Agent Benchmark is released under the Apache License 2.0.

