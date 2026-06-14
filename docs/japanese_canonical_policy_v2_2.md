# Japanese Canonical Policy v2.2

This document defines the Japanese-canonical language policy for Industrial Agent Benchmark v2.2.0 planning.

It is a planning document only. It does not modify benchmark data, translate tasks, update JSONL files, change schema implementation, or modify exporter, validator, or evaluation code.

## 1. Background

The latest released dataset baseline is v2.0.1.

| Layer | Count |
|---|---:|
| Knowledge | 60 |
| Reasoning | 60 |
| Agent | 60 |
| Total | 180 |

v2.1.0 multilingual architecture planning introduced item-level language metadata concepts and translation relationship policy.

The v2.2.0 language audits found:

| Classification | Count |
|---|---:|
| English-only | 45 |
| Japanese-only | 1 |
| Mixed-language | 134 |
| Total | 180 |

The largest field-level pattern is:

```text
Q=ja / C=ja / A=ja / R=mixed: 87
```

Project owner decision:

```text
The canonical language of Industrial Agent Benchmark is Japanese.
```

## 2. Canonical Language Policy

Japanese is the canonical language of Industrial Agent Benchmark.

Canonical benchmark records should be authored, reviewed, and maintained in Japanese. English records are treated as translated or derivative distributions, not as the source of truth.

This policy does not prohibit English translations. It defines Japanese as the authoritative version for benchmark meaning, rubric criteria, and future content governance.

## 3. Scope of v2.2.0

v2.2.0 should focus on Japanese-canonical normalization.

In scope:

- language normalization planning
- Japanese-canonical rubric normalization
- mixed-language pattern cleanup planning
- English-to-Japanese migration planning for English-only tasks
- metadata policy alignment with Japanese canonical records

Out of scope:

- external public feedback collection
- full English translation release
- benchmark item translation during this planning task
- code, exporter, validator, or schema implementation changes
- mutation of v2.0.1 release artifacts

## 4. Treatment of Mixed-Language Records

Mixed-language records should be eliminated from canonical dataset records.

Mixed language may exist only as an interim migration or audit classification. It should not be the final state for Japanese-canonical records.

For current mixed records, normalization should identify the cause:

- Japanese task body with English rubric keys or scoring terms
- Japanese task body with English JSON field requirements
- English question with Japanese context or answer
- Japanese task using accepted English manufacturing terms
- true bilingual content requiring human review

Accepted manufacturing terms such as ERP, MES, QMS, JSON, HIL, OEE, Cpk, SLA, and similar abbreviations may remain when they are standard technical terminology. Their presence alone should not make a canonical Japanese task mixed-language.

## 5. Rubric Language Policy

Rubrics for Japanese-canonical tasks should be Japanese.

Rubric normalization must preserve:

- scoring concepts
- numeric checks
- required evidence
- critical failures
- score caps
- structured output requirements
- controlled-action boundaries
- human approval and escalation requirements
- audit-trail requirements

Translation or normalization must not weaken, broaden, narrow, or otherwise alter the evaluation criteria.

Where a rubric contains machine-readable keys, the project should distinguish between:

- public Japanese rubric text for evaluators
- stable machine-readable judge fields for tooling

This distinction should be handled in a future schema or authoring design, not by silently changing current benchmark records.

## 6. Metadata Policy

For Japanese-canonical records, metadata should converge to:

| Field | Policy |
|---|---|
| `language` | `ja` |
| `source_language` | `ja` once the Japanese canonical text is established |
| `translation_role` | `unpaired` unless a reviewed translation relationship exists |
| `translation_group_id` | omitted for `unpaired` records |

English records should be treated as derivative translations only when a reviewed relationship to a Japanese canonical record exists.

Before that review exists, English records should not be assumed to be authoritative sources for future benchmark meaning.

## 7. Migration Order

### Phase 1: Normalize Japanese-body tasks with mixed rubrics

Start with the largest pattern:

```text
Q=ja / C=ja / A=ja / R=mixed: 87
```

These records already have Japanese task bodies and expected answers. The main work is rubric normalization.

### Phase 2: Clean up other mixed-field tasks

Review mixed-field tasks where question, context, answer, or rubric language differs.

Prioritize categories where wording changes can affect safety or scoring:

- Agent safety
- HIL boundary
- structured decision
- data integrity
- risk tradeoff

### Phase 3: Translate English-only tasks into Japanese

English-only records should be migrated through controlled English-to-Japanese translation.

Translation must preserve:

- benchmark intent
- task difficulty
- manufacturing terminology
- numeric values
- feasibility decisions
- approval boundaries
- critical failures
- rubric scoring criteria

### Phase 4: Establish Japanese canonical metadata

After normalization or translation review, assign:

```text
language: ja
source_language: ja
translation_role: unpaired
translation_group_id: omitted
```

Translation groups should be introduced only when reviewed English derivative records are added or linked.

### Phase 5: Consider English translation pairs

Only after Japanese canonical normalization should English translation pairs be considered.

English pairs should be generated from Japanese canonical records and should use reviewed `translation_group_id` relationships.

## 8. Acceptance Criteria

Japanese-canonical normalization is complete when:

- canonical dataset records contain no mixed-language task records
- Japanese task bodies and rubrics are internally consistent
- rubric criteria, numeric checks, critical failures, and controlled-action boundaries are preserved
- v2.0.1 reproducibility remains preserved
- historical release artifacts are not silently mutated
- future English records can be generated as translations from Japanese canonical records
- translated records are clearly separated from canonical source records
- unpaired canonical records omit `translation_group_id`

## 9. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Meaning drift during rubric normalization | Scores may no longer reflect the original intent. | Require rubric-by-rubric review and preserve scoring concepts. |
| Loss of scoring compatibility | Results before and after normalization may not be directly comparable. | Version the normalized release and document compatibility boundaries. |
| Over-normalizing manufacturing terminology | Japanese records may become less realistic or less usable. | Preserve standard industrial abbreviations and accepted technical terms. |
| Confusion between canonical and translated records | Users may compare source and derivative records incorrectly. | Use explicit metadata and translation-group policy. |
| English-only records become treated as source of truth | Canonical policy becomes ambiguous. | Establish Japanese canonical records before creating English derivatives. |
| Silent mutation of historical artifacts | v2.0.1 reproducibility may be broken. | Keep historical artifacts immutable and publish normalized records as a new version. |

## 10. Recommendation

v2.2.0 should be positioned as the Japanese-canonical normalization planning release.

The project should normalize the existing 180-task baseline toward Japanese canonical records before collecting broad public feedback or expanding into English translation pairs.

No translation or benchmark content modification should occur until a separate content-changing migration plan is approved.

