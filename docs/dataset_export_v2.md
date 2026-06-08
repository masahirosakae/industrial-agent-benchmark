# Dataset Export v2.0.0

This document describes the v2.0.0 prototype export from public benchmark YAML to Hugging Face-compatible JSONL.

## Source

The exporter reads public benchmark YAML files from:

```text
benchmark_data/
```

It does not modify benchmark question YAML files.

## Output

The exporter writes:

```text
data/v2/test.jsonl
```

The `test` split contains public benchmark questions.

## Schema

The output schema is defined in:

```text
docs/dataset_schema_v2.md
```

Every JSONL record must have exactly the v2 schema keys. Optional fields are still present with stable default values.

## Export Command

```bash
python scripts/export_hf_dataset_v2.py
```

## Validation

Validate the exported JSONL with:

```bash
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

The validator checks exact keys, stable field types, allowed task types, allowed difficulty values, and basic public-artifact exclusions.

## Local Loading

After exporting, load the local JSONL dataset with:

```bash
python examples/load_dataset_v2.py
```

This uses Hugging Face Datasets locally. Hosted loading from the Hugging Face Hub is planned but not required until the dataset is published.

## Exclusions

The exporter must not read or include:

- `results/`
- `results_v2/`
- judge outputs
- private reports
- raw model answers
- model-specific evaluation results
- provider names
- benchmark run artifacts

## Answer Field Policy

The v2 `answer` field is the public reference answer from the benchmark YAML. It is not a model output and must not be populated from generated answers, private runs, or judge results.
