# Simple Evaluation v2.0.0

Simple Evaluation v2 is a minimal HLE-style workflow for preparing standardized prediction files from pre-written answers.

This is not a leaderboard. It does not score answers automatically and does not call external APIs. Scoring and judge-based evaluation will be added later.

## Inputs

Dataset:

```text
data/v2/test.jsonl
```

Answers:

```text
examples/simple_eval_answers.jsonl
```

Answer format:

```json
{
  "id": "IA-HILB-001",
  "model_id": "sample_model",
  "answer": "..."
}
```

The answer file is matched to dataset records by `id`.

## Run Simple Evaluation

```bash
python eval/run_simple_eval.py \
  --dataset data/v2/test.jsonl \
  --answers examples/simple_eval_answers.jsonl \
  --model-id sample_model \
  --output-dir results/simple_eval/sample_model
```

Output:

```text
results/simple_eval/sample_model/predictions.jsonl
```

Prediction format:

```json
{
  "id": "IA-HILB-001",
  "model_id": "sample_model",
  "question": "...",
  "reference_answer": "...",
  "rubric": "...",
  "prediction": "...",
  "score": null,
  "score_method": "not_scored",
  "metadata": {}
}
```

Missing answers do not crash evaluation. They produce an empty `prediction` string.

## Summarize

```bash
python eval/summarize_simple_eval.py \
  --predictions results/simple_eval/sample_model/predictions.jsonl \
  --output results/simple_eval/sample_model/summary.json
```

Summary format:

```json
{
  "model_id": "sample_model",
  "num_questions": 140,
  "num_answered": 1,
  "num_missing": 139,
  "score_method": "not_scored"
}
```

## Validation Behavior

The runner validates:

- minimal dataset schema
- duplicate answer IDs
- unknown answer IDs
- model ID consistency
- answer record shape

Duplicate answer IDs fail clearly. Unknown answer IDs also fail clearly so the run does not silently evaluate answers for the wrong dataset.

## Artifact Policy

Generated outputs under `results/` are not committed. The public repository includes only the scripts, documentation, and toy example answer file.
