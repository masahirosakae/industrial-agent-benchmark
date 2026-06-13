# Hugging Face Publication Checklist

This checklist prepares Industrial Agent Benchmark v2.0.0 for Hugging Face Dataset publication. It documents the workflow only; do not publish automatically from this repository cleanup task.

## Publication Artifacts

- [ ] `dataset_card.md` is complete and renders as Markdown.
- [ ] `LICENSE_DATASET.md` is present.
- [ ] `data/v2/test.jsonl` exists.
- [ ] `docs/dataset_schema_v2.md` defines the schema.
- [ ] `docs/dataset_export_v2.md` documents the local export workflow.
- [ ] `scripts/validate_hf_dataset_v2.py` validates the JSONL file.

## Data Readiness

- [ ] Run `python scripts/export_hf_dataset_v2.py`.
- [ ] Run `python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl`.
- [ ] Confirm every record has exactly the v2 schema keys.
- [ ] Confirm `answer` contains public reference answers, not model outputs.
- [ ] Confirm no generated model answers are included.
- [ ] Confirm no per-run score files are included.
- [ ] Confirm no private run artifacts are included.

## Exclusions

Do not publish:

- `results/`
- `results_v2/`
- `datasets/results/`
- judge outputs
- raw model answers
- per-run reports
- private reports
- provider credentials
- internal model-name mappings
- local cache files

## Upload Workflow

Authenticate locally:

```bash
huggingface-cli login
```

Enable Git LFS if using a repository clone workflow:

```bash
git lfs install
```

Upload with `huggingface_hub`:

```python
from huggingface_hub import upload_folder

upload_folder(
    repo_id="masahirosakae/industrial-agent-benchmark",
    repo_type="dataset",
    folder_path="hf_dataset_upload",
)
```

The upload folder should contain only publication artifacts, for example:

```text
hf_dataset_upload/
  README.md
  LICENSE_DATASET.md
  data/
    v2/
      test.jsonl
```

Use `dataset_card.md` as the Hugging Face dataset `README.md` during upload.

## Validation Before Upload

Run:

```bash
python scripts/validate_dataset.py
python scripts/export_hf_dataset_v2.py
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

Optional local loading check after installing dependencies:

```bash
python examples/load_dataset_v2.py
```

## Publication Rules

- [ ] Do not create a leaderboard as part of dataset publication.
- [ ] Do not upload generated evaluation outputs.
- [ ] Do not upload private reports.
- [ ] Do not upload provider credentials.
- [ ] Do not upload local ignored directories.
- [ ] Record the published dataset version after upload.

## Post-Publication Checks

- [ ] Hosted `load_dataset` succeeds.
- [ ] Dataset card renders correctly on Hugging Face.
- [ ] Split names match documentation.
- [ ] License is visible.
- [ ] Repository README links to the hosted dataset only after publication.
