# Migration Plan v2.1

This document proposes the migration plan from Industrial Agent Benchmark v2.0.1 to the v2.1.0 multilingual architecture.

It is a planning document only. It does not modify benchmark data, JSONL exports, validation scripts, exporter scripts, or evaluation code.

## 1. Baseline

v2.0.1 is the baseline for migration.

| Property | Baseline |
|---|---|
| Total records | 180 |
| Knowledge | 60 |
| Reasoning | 60 |
| Agent | 60 |
| Split | `test` |
| Current schema | v2.0.x flat JSONL schema |
| Language state | English, Japanese, and mixed-language records |

v2.1.0 should preserve the 180-record baseline unless a separate expansion task is approved.

## 2. Migration Goals

- Add explicit multilingual metadata.
- Preserve existing item IDs.
- Preserve current benchmark data until translation work is separately approved.
- Avoid silent schema changes in v2.0.x artifacts.
- Enable per-language reporting and future translation groups.
- Keep Hugging Face Dataset compatibility.

## 3. Proposed Migration Phases

### Phase 1: Audit Current Records

Classify each record using:

- `question`
- `context`
- `answer`
- `rubric`

Output of the audit should include:

- proposed `language`
- proposed `source_language`
- confidence or review note
- whether the record appears eligible for translation grouping

No benchmark text should be changed in this phase.

### Phase 2: Metadata-Only Migration

Add item-level metadata in a future v2.1 schema:

```json
{
  "language": "en",
  "source_language": "unknown",
  "translation_role": "unpaired"
}
```

Default migration for legacy records:

| Field | Default |
|---|---|
| `language` | audit result: `en`, `ja`, or `mixed` |
| `source_language` | `unknown` unless provenance is reliable |
| `translation_group_id` | omit unless a reviewed source, translation, or adaptation group exists |
| `translation_role` | `unpaired` |

### Phase 3: Translation Group Review

Create `translation_group_id` only after human review confirms a relationship. Unpaired records should omit `translation_group_id`.

Review checks:

- same benchmark intent
- equivalent difficulty or documented adaptation
- equivalent rubric criteria
- equivalent critical failures
- preserved numeric constraints
- preserved safety and approval boundaries

### Phase 4: Translation or Adaptation Work

After metadata migration is stable, selected records may be translated or adapted.

New translated records should:

- receive a new item ID
- share a `translation_group_id` with the reviewed source
- use `translation_role: translation` or `adaptation`
- preserve layer, category, difficulty, and rubric intent unless explicitly reviewed

### Phase 5: Evaluation Reporting

Evaluation reports should add optional breakdowns by:

- `language`
- `source_language`
- `translation_role`
- `translation_group_id`
- layer
- category

Default scoring should remain item-based.

## 4. Schema and Tooling Impact

The current v2.0.x exporter and validator use exact schema keys. v2.1.0 metadata cannot be added to `data/v2/test.jsonl` without a versioned schema update.

Future implementation should:

- introduce a v2.1 schema document
- update exporter constants for v2.1 only
- update validator constants for v2.1 only
- preserve v2.0.x validation for historical artifacts
- document which JSONL file is canonical for v2.1

No exporter or validator changes are part of this planning task.

## 5. Hugging Face Migration

Recommended publication approach:

1. Keep existing v2.0.x dataset artifact reproducible.
2. Publish v2.1 metadata fields in a versioned dataset update.
3. Keep dataset-level metadata:

   ```yaml
   language:
     - en
     - ja
   ```

4. Explain that item-level `language` is authoritative for individual records.
5. Avoid nested multilingual objects for v2.1.0.

## 6. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Legacy records have unclear source language. | Use `source_language: unknown`. |
| Mixed records are over-interpreted as translation pairs. | Default to `translation_role: unpaired`. |
| Translation changes item difficulty. | Use human review and `adaptation` role when needed. |
| Evaluations compare non-equivalent tasks. | Only compare within reviewed translation groups. |
| v2.0.x tools fail on new fields. | Version schema, exporter, and validator. |
| HF users infer all rows are both languages. | Document dataset-level vs item-level language metadata. |

## 7. Acceptance Criteria

v2.1.0 multilingual migration is ready when:

- all 180 baseline records have proposed language metadata
- v2.0.x artifacts remain reproducible
- no benchmark item text is changed by metadata migration alone
- translation groups are reviewed before publication
- Hugging Face loading remains simple
- validation can distinguish v2.0.x and v2.1 schemas
- documentation describes the dataset as multilingual

## 8. Rollback Plan

If v2.1 migration creates ambiguity or tool incompatibility:

- keep v2.0.1 as the stable public baseline
- revert only the v2.1 metadata artifact
- preserve all original benchmark YAML and v2.0.x JSONL files
- publish a correction note explaining that language metadata requires further review
