# GitHub Release Checklist

## Repository Contents

- [ ] `LICENSE` is present and uses Apache License 2.0.
- [ ] `README.md` describes the project purpose, benchmark structure, evaluation links, and license.
- [ ] `docs/benchmark_spec.md` is present.
- [ ] `docs/difficulty_definition.md` is present.
- [ ] `docs/evaluation_methodology.md` is present.
- [ ] `docs/benchmark_release_notes_v1.0.md` is present.
- [ ] `docs/benchmark_card.md` is present.
- [ ] `benchmark_data/` is present and contains the v1.0 dataset.
- [ ] `scripts/validate_dataset.py` is present.

## Excluded Files

- [ ] `results/` is excluded.
- [ ] `judgements/` is excluded.
- [ ] aggregate score CSV files are excluded.
- [ ] internal evaluation reports are excluded.
- [ ] Python cache files are excluded.

## Content Review

- [ ] No personal information is present.
- [ ] No API keys or credentials are present.
- [ ] No local absolute paths are present.
- [ ] No private evaluation participation details are present.
- [ ] No private run summaries are present.
- [ ] No private benchmark run artifacts are present.

## Validation

- [ ] Run `python scripts/validate_dataset.py`.
- [ ] Confirm validation reports 90 problem files.
- [ ] Confirm validation reports zero errors.
- [ ] Confirm validation reports zero warnings.

## Release Notes

- [ ] Release notes describe dataset scope and methodology.
- [ ] Release notes do not include private run results.
- [ ] Release notes do not include private run summaries.
