# Judge Evaluation v2.0.0

Judge Evaluation v2 is the first deterministic scoring layer for Industrial Agent Benchmark v2.0.0.

This version is intentionally minimal:

- rule-based scoring only
- no external APIs
- no LLM judge
- deterministic
- score range 0-5
- not a leaderboard

The purpose is to establish the scoring pipeline and file format before adding an LLM judge later.

## Input

Judge Evaluation v2 reads Simple Evaluation v2 predictions:

```text
results/simple_eval/<model_id>/predictions.jsonl
```

Run:

```bash
python eval/run_judge_eval.py \
  --predictions results/simple_eval/sample_model/predictions.jsonl \
  --output-dir results/judge_eval/sample_model
```

## Output

The judge runner writes:

```text
results/judge_eval/<model_id>/judgements.jsonl
```

Judgement records use this format:

```json
{
  "id": "IA-HILB-001",
  "model_id": "sample_model",
  "score": 2,
  "score_method": "rule_based_token_overlap_v1",
  "prediction": "...",
  "reference_answer": "...",
  "rubric": "...",
  "metadata": {}
}
```

Scores are integers from 0 to 5. Empty predictions receive 0. Non-empty predictions receive a deterministic token-overlap score against the public reference answer and rubric.

## Summarize

```bash
python eval/summarize_judge_eval.py \
  --judgements results/judge_eval/sample_model/judgements.jsonl \
  --output results/judge_eval/sample_model/summary.json
```

The summary includes question count, answered count, average score, min/max score, and score distribution.

## Limitations

The rule-based score is a pipeline placeholder, not a final quality judgement. It is useful for validating file formats, deterministic scoring, and summary generation. It should not be treated as a leaderboard score.

Future versions may add judge prompts, rubric-aware scoring, numeric checks, or an LLM judge. Those additions must remain explicit and versioned.

## Artifact Policy

Generated outputs under `results/` are local artifacts and are not committed. The public repository includes only scripts, documentation, and toy examples.
