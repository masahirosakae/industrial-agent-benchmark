# Simple Evaluation Plan

This document defines the first v2.0.0 public evaluation workflow.

## Objective

Provide a simple local evaluation path before building a leaderboard. The first workflow should be easy to run, deterministic, and explicit about required local answer files.

## Workflow

1. Load or inspect the public dataset.
2. Generate answers outside the repository.
3. Store local answers in an ignored output directory.
4. Run the simple evaluator.
5. Write local metrics and reports to ignored output paths.

## Inputs

The evaluator should require:

- dataset version or dataset path
- answer directory or answer JSONL path
- output directory

Answer files must be produced by the user. The repository must not ship private answer files.

## Outputs

Evaluation outputs should be local generated artifacts, such as:

- per-question scores
- aggregate metrics
- simple markdown or JSON summary
- evaluator version metadata

Generated outputs must remain ignored by git unless they are hand-written examples explicitly approved for publication.

## Initial Scoring Scope

The first public evaluator should prioritize clarity over completeness:

- validate answer presence
- validate question IDs
- compute simple per-question and aggregate metrics when judge outputs are available
- fail clearly when required local inputs are missing

More complex judge automation and leaderboard submission should come later.

## Error Behavior

Missing answer files should not silently pass. The evaluator should explain:

- which local input is missing
- the expected answer layout
- which command validates the public dataset without answers

## Acceptance Criteria

- Fresh clone can validate the dataset without answers.
- Evaluation command fails clearly when answers are absent.
- Evaluation command writes only to ignored local output paths.
- Documentation contains no private model outputs or private result references.
