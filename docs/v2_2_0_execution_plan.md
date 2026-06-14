# v2.2.0 Execution Plan

This document defines the implementation plan for Japanese-canonical normalization of Industrial Agent Benchmark.

It is a planning document only. It does not modify benchmark content, translate tasks, update JSONL files, change schema implementation, or modify exporter, validator, or evaluation code.

Inputs:

- `docs/multilingual_architecture_v2_1.md`
- `docs/language_policy_v2_1.md`
- `docs/migration_plan_v2_1.md`
- `docs/language_audit_report_v2_2.md`
- `docs/language_normalization_plan_v2_2.md`
- `docs/japanese_canonical_policy_v2_2.md`

## 1. Objectives

The objective of v2.2.0 is to prepare and execute Japanese-canonical normalization while preserving benchmark integrity.

Primary objectives:

- establish Japanese as the canonical language for benchmark records
- eliminate mixed-language records from the canonical dataset
- preserve scoring meaning, numeric checks, critical failures, and controlled-action boundaries
- preserve v2.0.1 reproducibility
- avoid silent mutation of historical artifacts
- create a foundation for future English translations as derivative records

## 2. Scope

In scope for the eventual v2.2.0 implementation:

- field-level language review of all 180 tasks
- Japanese normalization of canonical task fields
- rubric language normalization
- metadata migration planning and future schema update
- validation of Japanese task consistency
- release documentation for compatibility boundaries

Current dataset baseline:

| Layer | Count |
|---|---:|
| Knowledge | 60 |
| Reasoning | 60 |
| Agent | 60 |
| Total | 180 |

Current audit baseline:

| Language class | Count |
|---|---:|
| English-only | 45 |
| Japanese-only | 1 |
| Mixed-language | 134 |
| Total | 180 |

Largest normalization pattern:

```text
Q=ja / C=ja / A=ja / R=mixed: 87
```

## 3. Out of Scope

Out of scope for v2.2.0 planning and the initial normalization execution:

- public feedback collection
- full English translation release
- creation of bilingual paired benchmark items
- leaderboard changes
- provider-specific evaluation
- generated model answers
- private evaluation outputs
- mutation of v2.0.1 historical artifacts
- unreviewed machine translation

English derivative releases should be considered only after Japanese canonical records are established.

## 4. Work Breakdown Structure

| WBS | Work item | Output | Owner type |
|---|---|---|---|
| 1.0 | Baseline freeze | Confirmed v2.0.1 artifact references and counts | Release maintainer |
| 2.0 | Field-level language audit | Per-record field classification | Dataset reviewer |
| 3.0 | Metadata preparation | Proposed `language`, `source_language`, `translation_role`, and optional `translation_group_id` | Dataset maintainer |
| 4.0 | Rubric normalization | Japanese rubrics for Japanese-body tasks | Domain reviewer |
| 5.0 | Mixed-field cleanup | Japanese-canonical task body and answer consistency | Domain reviewer |
| 6.0 | English-only migration | Reviewed English-to-Japanese canonical translations | Translator and domain reviewer |
| 7.0 | Validation | Schema, language, rubric, numeric, and safety checks | QA reviewer |
| 8.0 | Release packaging | v2.2.0 docs, dataset card notes, compatibility statement | Release maintainer |

## 5. Dataset Normalization Workflow

### Step 1: Freeze the baseline

Record the v2.0.1 baseline:

- 180 records
- Knowledge 60 / Reasoning 60 / Agent 60
- current IDs preserved
- current JSONL schema preserved as historical artifact

No normalization work should overwrite or silently mutate this baseline.

### Step 2: Normalize Japanese-body tasks with mixed rubrics

Start with:

```text
Q=ja / C=ja / A=ja / R=mixed: 87
```

Expected work:

- translate or normalize rubric text into Japanese
- preserve rubric criteria
- keep accepted manufacturing abbreviations when appropriate
- check score caps, numeric checks, disallowed answers, and critical failures

This is the highest-leverage first phase because the task body is already Japanese-canonical.

### Step 3: Clean up other mixed-field records

Handle records with mixed question, context, answer, or rubric fields.

Priority categories:

- Agent safety
- HIL boundary
- structured decision
- data integrity
- risk tradeoff

These categories require careful review because wording changes can affect safety, escalation, auditability, or reasoning constraints.

### Step 4: Translate English-only records into Japanese canonical form

Handle the 45 English-only records after rubric-normalization rules are stable.

High-priority English-only groups:

- `change_control`
- `numeric_capacity_planning`
- later `human_in_the_loop`
- later `workflow_design`

Each translation must preserve:

- benchmark intent
- difficulty
- numeric values
- feasibility decisions
- required evidence
- approval boundaries
- final-state requirements
- critical failures
- rubric scoring criteria

### Step 5: Review and lock canonical records

After normalization, each record should receive a review decision:

- approved as Japanese canonical
- needs rubric revision
- needs task-body revision
- needs numeric/safety review
- blocked pending owner decision

## 6. Metadata Migration Workflow

Future v2.2 implementation should align with v2.1 metadata planning.

For Japanese canonical records:

| Field | Target value |
|---|---|
| `language` | `ja` |
| `source_language` | `ja` once canonical Japanese text is established |
| `translation_role` | `unpaired` unless reviewed translation relationship exists |
| `translation_group_id` | omitted for `unpaired` records |

Migration sequence:

1. classify current record language
2. normalize canonical Japanese content
3. assign metadata after review
4. omit `translation_group_id` for unpaired canonical records
5. add translation group metadata only when English derivative records are reviewed

The current exact-key v2.0.x JSONL schema cannot accept these metadata fields without a versioned schema change. Schema implementation is a separate future task.

## 7. Validation Strategy

Validation should cover both structure and meaning.

### Structural validation

- all expected records are present
- IDs remain stable
- layer counts remain 60 / 60 / 60
- no unexpected schema drift
- no private artifacts or generated answers are included

### Language validation

- canonical records classify as Japanese
- no canonical record remains mixed-language
- Japanese task body and rubric are internally consistent
- accepted technical abbreviations are allowed and documented

### Rubric validation

- `must_have` criteria are preserved
- `nice_to_have` criteria are preserved where applicable
- `critical_failures` are preserved
- numeric checks and score caps are preserved
- controlled-action boundaries remain explicit
- audit-trail and human-approval requirements remain explicit

### Regression validation

- v2.0.1 can still be reproduced
- v2.2 artifacts are versioned separately
- result comparability caveats are documented

## 8. Rollback Strategy

If normalization introduces ambiguity or breaks compatibility:

1. keep v2.0.1 as the stable public baseline
2. revert the v2.2 normalized artifact
3. preserve all original benchmark YAML and v2.0.x JSONL files
4. retain the audit report as planning evidence
5. publish a correction note if needed

Rollback must never rewrite historical release tags or silently replace published artifacts.

## 9. Acceptance Criteria

v2.2.0 Japanese-canonical normalization is ready when:

- 180 records are preserved unless a separate expansion is approved
- Knowledge 60 / Reasoning 60 / Agent 60 is preserved
- canonical records have no mixed-language task records
- Japanese task bodies and rubrics are internally consistent
- scoring concepts, numeric checks, critical failures, and controlled-action boundaries are preserved
- English-only records are converted through reviewed English-to-Japanese translation
- v2.0.1 reproducibility remains preserved
- no historical release artifact is silently mutated
- future English records can be generated as translations from Japanese canonical records

## 10. Estimated Effort by Task Category

Effort estimates are planning estimates only.

| Category group | Records | Main work | Estimated effort |
|---|---:|---|---|
| Japanese-body tasks with mixed rubrics | 87 | Rubric normalization and scoring review | Medium |
| English-only tasks | 45 | Full English-to-Japanese translation and review | High |
| Mixed-field tasks | 47 | Field-by-field normalization and semantic review | Medium to high |
| Japanese-only task | 1 | Metadata and consistency review | Low |

Estimated effort by layer:

| Layer | Main work | Estimated effort |
|---|---|---|
| Knowledge | Rubric normalization plus English change-control translation | Medium |
| Reasoning | Rubric normalization, numeric preservation, risk/data-integrity review | High |
| Agent | Safety, HIL, workflow, and controlled-action wording review | High |

Recommended execution order:

1. Knowledge Japanese-body rubric normalization
2. Reasoning Japanese-body rubric normalization
3. Agent Japanese-body rubric normalization
4. Mixed-field safety and data-integrity records
5. English-only Knowledge records
6. English-only Reasoning records
7. English-only Agent records

