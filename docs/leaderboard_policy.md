# Leaderboard Policy

The v2.0.0 leaderboard is a later-stage feature. It should not be built before the dataset-loading and simple-evaluation workflow is stable.

## Principles

- Public reproducibility is required.
- Submissions must identify dataset and evaluator versions.
- Raw model answers should not be committed to the repository.
- Private provider credentials must never be included.
- Leaderboard publication should use reviewed, intentionally published summaries.

## Submission Requirements

Future leaderboard submissions should include:

- model display name approved for publication
- dataset version
- evaluator version
- scoring configuration
- aggregate metrics
- critical failure rate when available
- reproducibility notes

Submission packages should not include private credentials or unrelated local artifacts.

## Publication Rules

Leaderboard entries should be published only when:

- the dataset version is public
- the evaluator version is public
- the scoring method is documented
- the submitted summary is reproducible from accepted artifacts
- the model/provider naming is approved for public display

## Exclusions

Do not publish:

- raw local answer directories
- private result directories
- unpublished evaluation reports
- provider secrets
- internal model-name mappings
- results from unreleased or private evaluation runs

## Future Work

After simple evaluation is stable, define:

- leaderboard file format
- submission review process
- accepted metrics
- tie-breaking policy
- update cadence
- archival policy for older benchmark versions
