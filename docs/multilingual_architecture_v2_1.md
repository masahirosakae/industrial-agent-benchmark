# Multilingual Architecture v2.1

This document proposes the multilingual architecture for Industrial Agent Benchmark v2.1.0.

It is a planning document only. It does not modify benchmark data, JSONL exports, validation scripts, exporter scripts, or evaluation code.

## 1. Background

Industrial Agent Benchmark v2.0.1 is the migration baseline:

| Layer | Count |
|---|---:|
| Knowledge | 60 |
| Reasoning | 60 |
| Agent | 60 |
| Total | 180 |

The v2.0.x dataset contains English, Japanese, and mixed-language records. Dataset-level metadata now identifies the benchmark as English and Japanese, but individual records do not yet carry item-level language metadata.

v2.1.0 should formalize multilingual support without breaking v2.0.x reproducibility.

## 2. Design Principles

- Preserve the 180-item v2.0.1 baseline unless a separate content-expansion release is explicitly approved.
- Make language explicit at record level.
- Separate the published record language from the original authoring language.
- Do not infer translation equivalence without review.
- Keep Hugging Face Dataset loading simple and viewer-friendly.
- Keep evaluation compatibility clear across Knowledge, Reasoning, and Agent layers.
- Avoid private data, provider-specific evaluation results, and unpublished model outputs.

## 3. Proposed Metadata Fields

The following fields are proposed for a future v2.1 JSONL schema or migration layer.

| Field | Required | Type | Allowed values | Purpose |
|---|---:|---|---|---|
| `language` | Yes | string | `en`, `ja`, `mixed` | Language of the published benchmark record. |
| `source_language` | Yes | string | `en`, `ja`, `unknown` | Original authoring or source language, when known. |
| `translation_group_id` | No | string | Stable ID | Groups semantically related source, translation, and adaptation records. Present only when the item belongs to a reviewed group. |
| `translation_role` | Yes | string | `source`, `translation`, `adaptation`, `unpaired` | Relationship of the record within a translation group. |

### Field Semantics

`language` describes what the evaluator and model see in the published record.

`source_language` describes the known original authoring language. Legacy v2.0.x records should use `unknown` unless provenance is reliable. Do not use `mixed` for `source_language`; mixed publication language does not prove mixed original authorship.

`translation_group_id` is optional. It should be present only when the item belongs to a reviewed source, translation, or adaptation group. Unpaired records should omit `translation_group_id`.

When present, `translation_group_id` should be stable across releases. Recommended format:

```text
TG-<layer>-<category>-<number>
```

Examples:

```text
TG-IA-HIL-001
TG-IR-NCP-003
TG-IK-CC-010
```

`translation_role` identifies whether the item is the source item, a direct translation, a localized adaptation, or currently unpaired.

## 4. English and Japanese Task Relationship

v2.1.0 should distinguish four relationship states.

| Relationship | Meaning | Evaluation implication |
|---|---|---|
| `unpaired` | No reviewed equivalent in another language. | Score independently. |
| `source` | Canonical authored item in a group. | May be compared with reviewed translations. |
| `translation` | Direct semantic translation. | Scores may be compared within group if rubric alignment is confirmed. |
| `adaptation` | Same benchmark intent with localized detail or modified context. | Compare cautiously; do not assume identical difficulty. |

Existing v2.0.x records should initially be migrated as `unpaired` unless a human review confirms a translation relationship.

## 5. Translation Strategy

Recommended sequence:

1. Audit current records for `language`.
2. Assign `source_language`.
3. Mark all legacy records as `translation_role: unpaired`.
4. Create translation groups only after human semantic review.
5. Translate or adapt selected high-value records.
6. Validate rubric equivalence before using paired scores for cross-language comparisons.

Machine translation may be used as a draft aid, but final benchmark records should receive human review for manufacturing terminology, safety boundaries, numeric constraints, and rubric alignment.

## 6. Rubric Multilingual Architecture

Rubrics should be understandable in the same language as the task where possible. However, grading concepts must remain stable across language variants.

For translation groups, reviewers should confirm:

- required points are semantically equivalent
- critical failures are equivalent
- numeric checks are unchanged or intentionally adapted
- approval-boundary and safety language remains precise
- domain terminology is not weakened by translation

For Agent-layer items, translation must preserve controlled action boundaries, escalation requirements, final state expectations, and audit trail requirements.

## 7. Evaluation Pipeline Compatibility

v2.0.x validation and export scripts use an exact JSONL key list. Adding item-level language fields is a schema change and should not be silently introduced into v2.0.x exports.

v2.1.0 implementation should therefore introduce versioned schema handling:

- keep v2.0.x JSONL reproducible
- define v2.1 schema keys explicitly
- update exporter and validator only in a future implementation task
- update evaluation scripts to pass through language metadata without changing scoring behavior by default

Evaluation reporting should support optional breakdowns by:

- `language`
- `source_language`
- `translation_role`
- `translation_group_id`
- layer and category

## 8. Hugging Face Dataset Compatibility

The proposed fields are flat scalar columns and are compatible with Hugging Face Dataset Viewer.

Dataset-level metadata should remain:

```yaml
language:
  - en
  - ja
```

Item-level `language` should be the authoritative per-record language label. Dataset users should not infer every record's language from the dataset-level metadata.

Avoid nested multilingual objects for v2.1.0 because they complicate JSONL loading, viewer display, and downstream evaluation tooling.

## 9. Compatibility Analysis

| Area | Compatibility note |
|---|---|
| v2.0.x JSONL | Must remain unchanged and reproducible. |
| v2.1 JSONL | May add language metadata fields after schema update. |
| Existing IDs | Preserve existing item IDs. |
| Translation groups | Add grouping metadata; do not replace item IDs. |
| Benchmark counts | Preserve 180-item baseline unless content expansion is separately approved. |
| Evaluation | Scores remain item-based; group-level comparison is optional. |
| HF loading | Flat fields remain compatible with `datasets`. |

## 10. Risks and Tradeoffs

- `mixed` records may hide unclear authoring provenance; use `source_language: unknown` when provenance is uncertain.
- Direct translations may shift difficulty because manufacturing terminology and safety wording differ by language.
- Over-grouping can create false equivalence between adapted tasks.
- Per-language score reporting may expose model language-strength differences rather than industrial capability alone.
- Keeping v2.0.x reproducible requires parallel documentation of old and new schemas.

## 11. Recommended v2.1.0 Outcome

v2.1.0 should be described as the multilingual architecture release for Industrial Agent Benchmark.

It should not be described as English-only or Japanese-only. The correct public classification is:

```text
Multilingual Benchmark
```
