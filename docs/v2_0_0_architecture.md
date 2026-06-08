# v2.0.0 Architecture

v2.0.0 is the active development line for Industrial Agent Benchmark.

## Goal

v2.0.0 should make the benchmark easier to use from a fresh public environment. The target workflow follows the pattern used by public benchmark projects where the dataset is distributed through a dataset hub and the repository provides evaluation code, documentation, and policy.

## Architecture Direction

The v2.0.0 architecture has four layers:

| Layer | Responsibility |
|---|---|
| Dataset package | Public benchmark data distributed through Hugging Face Datasets. |
| GitHub repository | Evaluation scripts, documentation, validation tools, and versioned policies. |
| Simple evaluation | First runnable public evaluation path with local answer files and transparent outputs. |
| Leaderboard | Later-stage submission and publication process after the simple evaluation is stable. |

## HLE-Style Workflow

The intended workflow is:

1. Load the dataset with Hugging Face Datasets.
2. Generate model answers outside the repository.
3. Run simple evaluation scripts from GitHub.
4. Store local outputs outside committed source files.
5. Add leaderboard support only after evaluation behavior is stable and reproducible.

The repository must not contain private model evaluation artifacts.

## Public Data Flow

```text
Hugging Face dataset
  -> public dataset loader
  -> local answer generation by user
  -> GitHub evaluation script
  -> local metrics/report files
  -> optional later leaderboard submission
```

## Design Principles

- Public users should not need private answer directories to inspect or load the dataset.
- Evaluation scripts should fail clearly when required local answer files are missing.
- Simple evaluation should precede leaderboard design.
- Leaderboard results should be reproducible and tied to documented dataset and evaluator versions.
- Private model outputs, provider secrets, and unpublished reports must remain outside the repository.

## v2.0.0 Deliverables

Initial v2.0.0 work should produce:

- Hugging Face dataset packaging plan and dataset card
- stable public dataset schema
- simple local evaluation script
- documented input and output conventions
- public artifact policy
- leaderboard policy for later work
- versioning policy

## Non-Goals

v2.0.0 does not retroactively publish private v1.1.0 evaluation results. It also does not require a leaderboard before the dataset-loading and simple-evaluation workflow is stable.
