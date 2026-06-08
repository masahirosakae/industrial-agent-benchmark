# Public Repository Audit

Repository: `industrial-agent-benchmark`

Date: 2026-06-08

Scope: public-clone readiness for Industrial Agent Benchmark v1.1.0-pre. This audit focuses on whether a fresh public clone can validate and inspect the benchmark without unpublished answer/result artifacts.

## Fresh Clone Validation

Expected public-clone behavior:

1. Clone repository.
2. Install the only documented runtime dependency for validation:

   ```bash
   pip install pyyaml
   ```

3. Validate dataset:

   ```bash
   python scripts/validate_dataset.py
   ```

Expected result:

```text
Checked: 140 problem files
Errors: 0
Warnings:0
```

Fresh clones are not expected to contain:

- `results_v2/`
- `results/`
- `judgements/`
- raw model answers
- generated judge inputs
- judge outputs
- model-specific evaluation results
- private reports
- API keys, `.env` files, tokens, or provider credentials

## README Quick Start Validation

The README Quick Start has been changed to a public-safe flow:

1. Install `pyyaml`.
2. Run `python scripts/validate_dataset.py`.
3. Inspect public YAML question files.
4. Treat Judge v2 input generation as an advanced workflow that requires locally generated answer files.

Judge v2 input generation is now documented with its prerequisite:

```text
results_v2/<model_id>/answers/<question_id>.txt
```

`results_v2/` is intentionally excluded from the public repository. The README no longer presents `python scripts/prepare_judge_inputs_v2.py model_a` as a fresh-clone Quick Start command.

## Public Artifact Review

Public-safe artifacts:

- `benchmark_data/`
- `evaluation_set_v1.yaml`
- `evaluation_set_v2.yaml`
- `judge_template.md`
- `judge_template_v2.md`
- `scripts/generate_dataset.py`
- `scripts/validate_dataset.py`
- `scripts/prepare_judge_inputs_v2.py`
- public benchmark documentation under `docs/`

Artifacts that must remain absent from the public repository:

- raw model answers
- `results_v2/`
- `results/`
- judge outputs
- model-specific evaluation results
- unpublished evaluation reports
- provider/model-name mappings
- API keys and secrets

Local workspace note: ignored/generated directories such as `results_v2/`, `datasets/results/`, and `evaluation_reports/` may exist locally, but they should not be committed or published.

## Directory Structure Review

Expected public structure:

```text
industrial-agent-benchmark/
  benchmark_data/
    index.yaml
    index.csv
    knowledge/
    reasoning/
    agent/
  docs/
  scripts/
    generate_dataset.py
    validate_dataset.py
    prepare_judge_inputs_v2.py
  evaluation_set_v1.yaml
  evaluation_set_v2.yaml
  judge_template.md
  judge_template_v2.md
  README.md
  README_EN.md
  .gitignore
```

Public repository hygiene requirements:

- `results_v2/` must be absent from git and ignored.
- `results/` must be absent from git and ignored.
- `datasets/results/` must be absent from git and ignored.
- `evaluation_reports/` must be absent from git and ignored unless a specific report is approved for publication.
- `__pycache__/` and `*.pyc` must be absent from git and ignored.
- `.env`, `.env.*`, `*.key`, and `*.pem` must be absent from git and ignored.

## Sample Data Strategy

Recommended future public sample layout:

```text
examples/
  sample_answers/
    sample_model/
      answers/
        IK-MAINT-001.txt
        IA-HILB-001.txt
  sample_judge_inputs/
```

Sample answers should be short, hand-written toy responses. They must not be real model outputs and must not reproduce private evaluation artifacts.

The existing script already accepts a custom results root:

```bash
python scripts/prepare_judge_inputs_v2.py sample_model --results-root examples/sample_answers
```

If sample data is added later, include only toy answers and document that the generated judge inputs are examples, not benchmark results.

## Severity-Ranked Findings

### Finding 1

Severity: High

Finding: README Quick Start documents prepare_judge_inputs_v2.py model_a as if it works on fresh clone.

Impact: Fresh clone fails because results_v2/model_a/answers does not exist.

Fix: Move Judge v2 input generation to an advanced/private workflow section, or provide public sample answers under examples/sample_answers.

Status: Fixed in `README.md` and mirrored in `README_EN.md`. Judge v2 input generation is now documented as requiring local answer files.

### Finding 2

Severity: High

Finding: Historical evaluation documents under `docs/` referenced anonymous model evaluation runs, generated answer workflows, and `results_v2/` paths.

Impact: Even anonymized model IDs can expose references to unreleased evaluation work or imply that unavailable private artifacts are part of the public release.

Fix: Before publication, either remove these historical execution reports from the public branch or move them to a private/internal documentation area. Candidate files include model-specific generation, trial judgement, and results-report docs.

Status: Fixed for the public tree by removing the tracked historical execution/result docs and adding ignore rules to prevent accidental re-addition.

### Finding 3

Severity: Medium

Finding: `.gitignore` was hard to read and did not include common secret-file patterns.

Impact: Reviewers could miss private-output rules, and local secret files were not explicitly ignored.

Fix: Reformat `.gitignore` into sections and add `.env`, `.env.*`, `*.key`, and `*.pem`.

Status: Fixed.

### Finding 4

Severity: Medium

Finding: `scripts/prepare_judge_inputs_v2.py` failed with only a terse missing-directory error.

Impact: Fresh-clone users could interpret expected missing private answers as a broken repository.

Fix: Keep the failure, but explain that the command requires answer files and point public users to dataset validation.

Status: Fixed.

### Finding 5

Severity: Medium

Finding: Public sample answers are not available.

Impact: Users cannot exercise Judge v2 input generation end to end from a fresh clone without first producing their own answers.

Fix: Add hand-written toy sample answers under `examples/sample_answers` and document `--results-root examples/sample_answers`.

Status: Recommended, not implemented.

### Finding 6

Severity: Low

Finding: `README_EN.md` was absent.

Impact: If external docs or users expect an English README, they encounter a missing file.

Fix: Add `README_EN.md` mirroring the public-safe Quick Start.

Status: Fixed.

## Reproduction Steps

### Fresh-Clone Validation

```bash
pip install pyyaml
python scripts/validate_dataset.py
```

Expected:

```text
Checked: 140 problem files
Errors: 0
Warnings:0
```

### README Quick Start Failure Before Fix

Before the README fix, a public user would run:

```bash
python scripts/prepare_judge_inputs_v2.py model_a
```

On a fresh clone without private results, this fails because:

```text
results_v2/model_a/answers
```

does not exist.

### Expected Judge v2 Failure After Fix

The command should still fail if answers are absent:

```bash
python scripts/prepare_judge_inputs_v2.py model_a
```

Expected behavior: non-zero exit with a clear message explaining that answer files are required and that the public Quick Start command is:

```bash
python scripts/validate_dataset.py
```

## Recommended Fixes

1. Keep README Quick Start limited to dependency installation, dataset validation, and public question inspection.
2. Keep Judge v2 input generation in a prerequisite-based workflow section.
3. Add hand-written toy sample answers only if end-to-end Judge v2 sample generation is desired.
4. Remove or privatize tracked historical model-evaluation execution reports before public release.
5. Keep `.gitignore` explicit about generated outputs, private reports, Python caches, and secret files.
6. Run the final validation commands immediately before tagging or publishing v1.1.0-pre.

## Final Validation Commands

Run or document the following before public release:

```bash
python scripts/validate_dataset.py
python scripts/generate_dataset.py
python scripts/validate_dataset.py
python scripts/prepare_judge_inputs_v2.py model_a
```

Expected result:

- `validate_dataset.py` passes.
- `generate_dataset.py` regenerates index files without unexpected diffs.
- `prepare_judge_inputs_v2.py model_a` fails with a clear expected message unless answers exist.

## v1.1.0-pre Public Release Checklist

- [ ] Fresh clone completes.
- [ ] README Quick Start has no missing-artifact commands.
- [ ] Dataset validation passes.
- [ ] `evaluation_set_v2.yaml` references existing question IDs.
- [ ] Judge v2 workflow clearly states answer-file prerequisite.
- [ ] `results_v2/` is absent from git and ignored.
- [ ] `results/` is absent from git and ignored.
- [ ] No raw model answers are committed.
- [ ] No judge outputs are committed.
- [ ] No private reports are committed.
- [ ] No API keys, `.env`, tokens, or provider secrets are committed.
- [ ] No unreleased model names or model-ID mapping are exposed.
- [ ] README and docs consistently describe v1.1.0-pre public scope.
