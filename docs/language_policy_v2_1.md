# Language Policy v2.1

This document defines the proposed language policy for Industrial Agent Benchmark v2.1.0.

It is a planning document only. It does not modify benchmark data, JSONL exports, validation scripts, exporter scripts, or evaluation code.

## 1. Policy Summary

Industrial Agent Benchmark v2.1.0 should be treated as a multilingual benchmark architecture.

The v2.0.1 baseline contains English, Japanese, and mixed-language records. v2.1.0 should make this explicit through item-level language metadata and clear authoring rules.

## 2. Language Classification

Each published record should have a `language` value.

| Value | Meaning |
|---|---|
| `en` | The task text, reference answer, and rubric are primarily English. |
| `ja` | The task text, reference answer, and rubric are primarily Japanese. |
| `mixed` | The record contains substantial English and Japanese content, or language differs materially across question, context, answer, and rubric. |

Classification should consider:

- `question`
- `context`
- `answer`
- `rubric`

Structural field names, JSON keys, IDs, tags, units, and short technical identifiers should not by themselves make a record `mixed`.

## 3. Source Language Policy

Each record should have a `source_language` value.

| Value | Meaning |
|---|---|
| `en` | The item was originally authored in English. |
| `ja` | The item was originally authored in Japanese. |
| `unknown` | The original authoring language cannot be confidently established. |

Use `unknown` for legacy records unless provenance is reliable.

Do not use `mixed` for `source_language`. A mixed published record does not prove mixed original authorship.

## 4. Translation Relationship Policy

Each record should have a `translation_role` value.

| Value | Meaning |
|---|---|
| `source` | Canonical authored record within a translation group. |
| `translation` | Direct semantic translation of a source record. |
| `adaptation` | Localized or modified version with the same benchmark intent. |
| `unpaired` | No reviewed translation relationship has been established. |

`translation_group_id` is optional. It should be present only when the item belongs to a reviewed source, translation, or adaptation group. `unpaired` records should omit `translation_group_id`.

## 5. Authoring Policy

New records should state their intended language before review.

Required authoring checks:

- question, context, answer, and rubric must be internally consistent
- domain terminology must be clear in the record language
- units and numeric constraints must be preserved
- human approval boundaries must remain explicit
- critical failures must not be weakened by translation
- public-safe wording must be maintained

## 6. Translation Policy

Direct translations should preserve:

- benchmark intent
- difficulty
- required reasoning path
- numeric values
- controlled action boundaries
- expected final state
- critical failures
- rubric scoring concepts

Adaptations may change local details, examples, or phrasing, but must be labeled `adaptation`.

Translation review should be performed before records are treated as paired for evaluation analysis.

## 7. Rubric Language Policy

Rubrics should normally be in the same language as the task. A task may still be `mixed` if the prompt is in one language while rubric content remains substantially in another language.

Rubric translation must preserve:

- `must_have` criteria
- `nice_to_have` criteria
- `critical_failures`
- score caps
- numeric checks
- structured output requirements
- disallowed answers

Judge implementation details may use English field names, but public scoring text should be understandable to the intended evaluator.

## 8. Evaluation Language Policy

Model answers should normally follow the task language unless the prompt explicitly asks otherwise.

Evaluation should not penalize a correct answer solely for using English or Japanese if:

- the answer is understandable
- required evidence and constraints are present
- the rubric does not require a specific language

For language-sensitive evaluation, reports should separate:

- industrial correctness
- language compliance
- translation equivalence

This avoids conflating model language ability with industrial reasoning ability.

## 9. Public Metadata Policy

Repository and Hugging Face metadata should identify the dataset as English and Japanese:

```yaml
language:
  - en
  - ja
```

Documentation should describe the benchmark as multilingual, not English-only.

Dataset users should rely on item-level `language` once v2.1 metadata exists.

## 10. v2.1.0 Acceptance Criteria

The language policy is ready when:

- every record can be classified as `en`, `ja`, or `mixed`
- every record can be assigned `source_language: en`, `ja`, or `unknown`
- every record can be assigned `translation_role`
- translation groups are created only after review
- public docs do not describe the dataset as English-only
- evaluation reporting can break down results by language without changing default scores
