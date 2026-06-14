# Language Normalization Plan v2.2

This document audits the current 180-task dataset and prepares a Japanese-canonical language normalization strategy.

It is an audit and planning document only. It does not translate benchmark tasks, modify benchmark content, update JSONL files, or change exporter, validator, or evaluation code.

## 1. Objective

Industrial Agent Benchmark canonical language is Japanese.

The v2.2 language normalization objective is to understand the current field-level language state and plan a migration path toward a Japanese-canonical dataset while preserving benchmark meaning, rubric quality, and evaluation compatibility.

## 2. Scope

Audit target:

```text
data/v2/test.jsonl
```

Audited fields:

- `question`
- `context`
- `answer`
- `rubric`

Dataset baseline:

| Layer | Count |
|---|---:|
| Knowledge | 60 |
| Reasoning | 60 |
| Agent | 60 |
| Total | 180 |

## 3. Classification Method

Each audited field was classified as:

| Label | Meaning |
|---|---|
| `en` | Primarily English field content. |
| `ja` | Primarily Japanese field content. |
| `mixed` | Substantial English and Japanese content in the field. |
| `none` | Empty or no detectable English/Japanese script. |

The audit used character-script detection across Japanese scripts and Latin letters. The result is useful for migration planning, but human review is still required before content normalization.

## 4. Field-Level Counts

| Field | en | ja | mixed | none | Total |
|---|---:|---:|---:|---:|---:|
| `question` | 57 | 93 | 30 | 0 | 180 |
| `context` | 45 | 113 | 22 | 0 | 180 |
| `answer` | 45 | 91 | 44 | 0 | 180 |
| `rubric` | 46 | 0 | 134 | 0 | 180 |

Key observation:

- The largest normalization issue is the rubric field: 134 records have mixed-language rubrics and 46 have English rubrics.
- No rubric field is classified as fully Japanese.
- 45 records are fully English across `question`, `context`, `answer`, and `rubric`.

## 5. Pattern Counts

Pattern notation:

```text
Q = question
C = context
A = expected answer
R = rubric
```

| Pattern | Count |
|---|---:|
| Q=ja / C=ja / A=ja / R=mixed | 87 |
| Q=en / C=en / A=en / R=en | 45 |
| Q=mixed / C=mixed / A=mixed / R=mixed | 14 |
| Q=mixed / C=ja / A=mixed / R=mixed | 12 |
| Q=en / C=ja / A=mixed / R=mixed | 9 |
| Q=ja / C=ja / A=mixed / R=mixed | 3 |
| Q=en / C=mixed / A=mixed / R=mixed | 3 |
| Q=ja / C=mixed / A=mixed / R=mixed | 2 |
| Q=mixed / C=ja / A=ja / R=mixed | 2 |
| Q=ja / C=mixed / A=ja / R=mixed | 1 |
| Q=mixed / C=mixed / A=mixed / R=en | 1 |
| Q=mixed / C=mixed / A=ja / R=mixed | 1 |
| Total | 180 |

## 6. Pattern Counts by Layer

### Knowledge

| Pattern | Count |
|---|---:|
| Q=ja / C=ja / A=ja / R=mixed | 45 |
| Q=en / C=en / A=en / R=en | 12 |
| Q=mixed / C=ja / A=ja / R=mixed | 2 |
| Q=mixed / C=mixed / A=ja / R=mixed | 1 |
| Total | 60 |

### Reasoning

| Pattern | Count |
|---|---:|
| Q=ja / C=ja / A=ja / R=mixed | 28 |
| Q=en / C=en / A=en / R=en | 12 |
| Q=en / C=ja / A=mixed / R=mixed | 8 |
| Q=mixed / C=ja / A=mixed / R=mixed | 7 |
| Q=mixed / C=mixed / A=mixed / R=mixed | 3 |
| Q=en / C=mixed / A=mixed / R=mixed | 2 |
| Total | 60 |

### Agent

| Pattern | Count |
|---|---:|
| Q=en / C=en / A=en / R=en | 21 |
| Q=ja / C=ja / A=ja / R=mixed | 14 |
| Q=mixed / C=mixed / A=mixed / R=mixed | 11 |
| Q=mixed / C=ja / A=mixed / R=mixed | 5 |
| Q=ja / C=ja / A=mixed / R=mixed | 3 |
| Q=ja / C=mixed / A=mixed / R=mixed | 2 |
| Q=ja / C=mixed / A=ja / R=mixed | 1 |
| Q=en / C=ja / A=mixed / R=mixed | 1 |
| Q=en / C=mixed / A=mixed / R=mixed | 1 |
| Q=mixed / C=mixed / A=mixed / R=en | 1 |
| Total | 60 |

## 7. Pattern Counts by Category

| Layer | Category | Dominant pattern | Count summary |
|---|---|---|---|
| Agent | `agent_design` | Q=ja / C=ja / A=ja / R=mixed | 4 mixed-rubric Japanese tasks |
| Agent | `agent_safety` | Q/C/A/R mixed | 5 mixed tasks |
| Agent | `hil_boundary` | mixed patterns | 5 mixed tasks |
| Agent | `human_in_the_loop` | Q=en / C=en / A=en / R=en | 10 English tasks, 3 mixed/Japanese tasks |
| Agent | `mcp` | mixed answer/rubric patterns | 3 mixed tasks |
| Agent | `multi_agent_coordination` | Q=ja / C=ja / A=ja / R=mixed | 3 mixed-rubric Japanese tasks |
| Agent | `structured_decision` | mixed patterns | 5 mixed tasks |
| Agent | `tool_selection` | mixed and English | 1 English task, 2 mixed tasks |
| Agent | `tool_trajectory` | mixed patterns | 5 mixed tasks |
| Agent | `workflow_design` | Q=en / C=en / A=en / R=en | 10 English tasks, 4 mixed-rubric Japanese tasks |
| Knowledge | `change_control` | Q=en / C=en / A=en / R=en | 10 English tasks |
| Knowledge | `improvement` | mixed-rubric Japanese | 1 English task, 4 mixed-rubric Japanese tasks |
| Knowledge | `maintenance_engineering` | mixed-rubric Japanese | 10 mixed tasks |
| Knowledge | `manufacturing_execution` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Knowledge | `manufacturing_preparation` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Knowledge | `order` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Knowledge | `procurement` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Knowledge | `production_planning` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Knowledge | `quality` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Knowledge | `shipping` | mixed-rubric Japanese | 1 English task, 4 mixed-rubric Japanese tasks |
| Reasoning | `5why` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Reasoning | `abnormality_analysis` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Reasoning | `capa` | mixed-rubric Japanese | 1 English task, 4 mixed-rubric Japanese tasks |
| Reasoning | `data_integrity` | mixed patterns | 10 mixed tasks |
| Reasoning | `fmea` | mixed-rubric Japanese | 1 English task, 4 mixed-rubric Japanese tasks |
| Reasoning | `fta` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Reasoning | `numeric_capacity_planning` | Q=en / C=en / A=en / R=en | 10 English tasks |
| Reasoning | `quality_improvement` | Q=ja / C=ja / A=ja / R=mixed | 5 mixed-rubric Japanese tasks |
| Reasoning | `risk_tradeoff` | English question with Japanese/mixed context and answer | 10 mixed tasks |

## 8. Mixed-Language Pattern Types

### JA task + EN metadata or rubric structure

Most common pattern:

```text
Q=ja / C=ja / A=ja / R=mixed
```

Count: 87

This is the lowest-effort normalization group. The task body is already Japanese-canonical, but rubric content contains English keys, scoring terms, or mixed field structures.

### EN task + EN rubric

Pattern:

```text
Q=en / C=en / A=en / R=en
```

Count: 45

This group requires full Japanese translation or bilingual pairing if the canonical dataset must be Japanese.

### EN question + JA context + mixed answer/rubric

Pattern:

```text
Q=en / C=ja / A=mixed / R=mixed
```

Count: 9

This group should be reviewed carefully because prompt language and scenario language differ.

### Mixed task + mixed rubric

Patterns include:

```text
Q=mixed / C=mixed / A=mixed / R=mixed
Q=mixed / C=ja / A=mixed / R=mixed
Q=en / C=mixed / A=mixed / R=mixed
```

Combined count: 29

These items need human review to determine whether English technical terms should remain as domain terms or be translated.

## 9. Normalization Effort Estimate

| Work type | Records | Effort | Description |
|---|---:|---|---|
| Rubric-only Japanese normalization | 87 | Low to medium | Main task content is Japanese; normalize rubric text while preserving judge criteria. |
| Full English-to-Japanese task translation | 45 | High | Translate question, context, answer, and rubric; review industrial terminology and scoring equivalence. |
| Mixed-field normalization | 47 | Medium to high | Resolve field-level language inconsistencies and decide which English terms remain accepted technical terms. |
| Japanese-only review | 1 | Low | Confirm consistency and add language metadata. |

Total records needing some normalization action:

```text
180 / 180
```

Reason: even Japanese task bodies currently have mixed or English rubrics, and no item-level language metadata exists.

## 10. Recommended Migration Order

### Phase 1: Metadata audit and freeze

Assign planned metadata without changing content:

- `language`
- `source_language`
- `translation_role`
- optional `translation_group_id`

For current records, default to:

```text
translation_role: unpaired
translation_group_id: omitted
```

### Phase 2: Rubric normalization for Japanese-body tasks

Start with the 87 records classified as:

```text
Q=ja / C=ja / A=ja / R=mixed
```

This produces the fastest progress toward Japanese-canonical consistency while minimizing translation risk.

### Phase 3: Normalize high-impact mixed categories

Prioritize:

- Agent safety
- HIL boundary
- structured decision
- data integrity
- risk tradeoff

These categories have safety, escalation, audit, or reasoning implications where translation must preserve exact constraints.

### Phase 4: Translate English-only task groups

Translate English-only categories after rubric normalization patterns are established.

High-priority English-only groups:

- `change_control` 10 records
- `numeric_capacity_planning` 10 records
- later `human_in_the_loop` records
- later `workflow_design` records

### Phase 5: Human review and validation

Every normalized record should be reviewed for:

- manufacturing terminology
- numeric equivalence
- approval-boundary meaning
- audit-trail requirements
- rubric criteria
- critical failures
- difficulty preservation

### Phase 6: Optional bilingual expansion

After Japanese-canonical normalization, the project may add English translations as reviewed paired records or provide parallel bilingual releases.

This should be separate from normalization of the current 180-task baseline.

## 11. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Rubric translation changes scoring standard. | Breaks score comparability. | Preserve must-have, nice-to-have, critical failures, score caps, and numeric checks. |
| English technical terms are over-translated. | Reduces manufacturing realism. | Maintain accepted terms such as ERP, MES, QMS, JSON, HIL, OEE when appropriate. |
| Japanese canonical text diverges from English originals. | Changes benchmark meaning. | Require human review for all translated records. |
| Mixed records are normalized mechanically. | May hide real bilingual requirements. | Classify mixed subtypes before editing content. |
| Evaluation scripts assume English rubric keys. | Tool compatibility risk. | Separate public rubric language from machine-readable judge fields in future schema design. |
| Public users compare pre- and post-normalization scores directly. | Misleading benchmark history. | Version the normalized release clearly and document non-equivalence if content changes. |

## 12. Recommendation

The current dataset should not be treated as language-normalized.

Because the canonical language is Japanese, the recommended next step is:

1. add item-level language metadata in planning
2. normalize Japanese-body task rubrics first
3. review mixed-field records by risk category
4. translate English-only tasks into Japanese
5. only then collect broad public feedback or expand into bilingual paired records

No translation should be performed until the project approves a content-changing migration plan.

