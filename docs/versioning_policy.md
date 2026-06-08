# Versioning Policy

Industrial Agent Benchmark uses versioned dataset and evaluation artifacts so public users can reproduce results and understand compatibility boundaries.

## Version Lines

| Version line | Status | Policy |
|---|---|---|
| v1.0 | Public baseline | Historical baseline. |
| v1.1.0 | Frozen pre-release snapshot | Public snapshot for inspection and compatibility; no active evaluation-result cleanup. |
| v2.0.0 | Active development | New architecture line for Hugging Face dataset loading, simple evaluation, and later leaderboard support. |

## Compatibility Rules

- Patch updates may clarify documentation or fix validation bugs without changing benchmark meaning.
- Minor updates may add public questions, metadata, or evaluation helpers while preserving documented compatibility.
- Major updates may change dataset layout, evaluation flow, or leaderboard policy.

## Dataset Versioning

Each public dataset release should document:

- dataset version
- schema version
- question count
- split names
- evaluator compatibility
- known limitations

## Evaluator Versioning

Evaluation outputs should record:

- evaluator version
- dataset version
- scoring mode
- timestamp
- local configuration needed for reproduction

Evaluator versions should be stable enough that leaderboard submissions can be compared fairly.

## Artifact Policy

Public versioned artifacts may include:

- benchmark questions
- public metadata
- public schemas
- evaluator scripts
- aggregate public leaderboard summaries

Public versioned artifacts must not include:

- raw model answers
- private result directories
- unpublished judge outputs
- provider credentials
- internal model-name mappings

## v1.1.0 Freeze

v1.1.0 remains available as a frozen pre-release benchmark snapshot. New architecture, dataset-distribution work, simple evaluation design, and leaderboard policy belong to v2.0.0.
