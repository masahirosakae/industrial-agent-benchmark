# v1.1.0 Freeze Note

v1.1.0 is frozen as a pre-release benchmark snapshot.

## Status

The v1.1.0 line is no longer the active development line. Its public dataset, evaluation set, judge templates, and validation scripts remain available as a snapshot for inspection, compatibility checks, and historical reference.

Active architecture work moves to v2.0.0.

## Frozen Public Scope

The frozen v1.1.0 snapshot includes:

- benchmark problem YAML files under `benchmark_data/`
- `benchmark_data/index.yaml`
- `benchmark_data/index.csv`
- `evaluation_set_v1.yaml`
- `evaluation_set_v2.yaml`
- `judge_template.md`
- `judge_template_v2.md`
- public validation and dataset-generation scripts
- public benchmark documentation

## Out of Scope

The freeze does not continue private evaluation-result cleanup. The v1.1.0 line should not add, publish, or reconstruct:

- raw model answers
- private result directories
- judge outputs
- model-specific evaluation reports
- provider or model-name mappings
- unpublished evaluation artifacts

## Maintenance Policy

Allowed maintenance on v1.1.0 is limited to:

- fixing public documentation that is misleading or unsafe
- fixing validation bugs that prevent public dataset inspection
- clarifying that generated answer/result artifacts are private and excluded

New benchmark architecture, dataset-distribution changes, public evaluation flows, and leaderboard design belong to v2.0.0.
