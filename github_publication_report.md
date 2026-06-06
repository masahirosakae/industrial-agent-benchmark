# GitHub Publication Preparation Report

## Summary

Industrial Agent Benchmark has been prepared for publication as an independent open source benchmark project.

## Completed Items

- Added Apache License 2.0 in `LICENSE`.
- Added `.gitignore` rules for generated and private evaluation artifacts.
- Added `docs/benchmark_card.md`.
- Added `github_release_checklist.md`.
- Moved release notes into `docs/benchmark_release_notes_v1.0.md`.
- Updated public documentation to use neutral evaluator wording.
- Reviewed public-facing files for restricted private run content.

## Public Documentation

Public documentation is intended to include:

- `README.md`
- `docs/benchmark_spec.md`
- `docs/difficulty_definition.md`
- `docs/evaluation_methodology.md`
- `docs/benchmark_release_notes_v1.0.md`
- `docs/benchmark_card.md`

## Excluded Artifacts

The following are excluded from publication by `.gitignore`:

- generated result directories
- judging output directories
- aggregate score files
- internal evaluation reports
- Python cache files

## Audit Result

No public-facing documentation should contain private run details, credentials, local absolute paths, or private run summaries.

Before publishing, run the checklist in `github_release_checklist.md` and the dataset validator.
