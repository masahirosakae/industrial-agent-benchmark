# Language Audit Report v2.2

This document audits the language distribution of the current Industrial Agent Benchmark dataset.

It is an audit and planning document only. It does not translate tasks, modify benchmark content, update JSONL files, or change exporter, validator, or evaluation code.

## 1. Scope

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

## 2. Classification Method

Each record was classified as:

| Label | Meaning |
|---|---|
| `en` | Primarily English across the audited fields. |
| `ja` | Primarily Japanese across the audited fields. |
| `mixed` | Substantial English and Japanese content both appear across the audited fields. |

The audit used a script-based character classification:

- Japanese characters: hiragana, katakana, CJK ideographs, and compatibility ideographs.
- English characters: Latin `A-Z` and `a-z`.
- Records with both Japanese and English at substantial levels were classified as `mixed`.
- Structural field names, IDs, short units, and JSON/YAML keys can contribute Latin characters; this means some Japanese prompt records with English rubric keys are classified as `mixed`.

This classification is useful for release planning, not a substitute for human language-policy review.

## 3. Total Counts

| Language label | Count | Share |
|---|---:|---:|
| `en` | 45 | 25.0% |
| `ja` | 1 | 0.6% |
| `mixed` | 134 | 74.4% |
| Total | 180 | 100.0% |

Japanese-inclusive records:

```text
ja + mixed = 135 / 180 = 75.0%
```

## 4. Counts by Layer

| Layer | en | ja | mixed | Total |
|---|---:|---:|---:|---:|
| Knowledge | 12 | 1 | 47 | 60 |
| Reasoning | 12 | 0 | 48 | 60 |
| Agent | 21 | 0 | 39 | 60 |
| Total | 45 | 1 | 134 | 180 |

## 5. Counts by Category

| Layer | Category | en | ja | mixed | Total |
|---|---|---:|---:|---:|---:|
| Agent | `agent_design` | 0 | 0 | 4 | 4 |
| Agent | `agent_safety` | 0 | 0 | 5 | 5 |
| Agent | `hil_boundary` | 0 | 0 | 5 | 5 |
| Agent | `human_in_the_loop` | 10 | 0 | 3 | 13 |
| Agent | `mcp` | 0 | 0 | 3 | 3 |
| Agent | `multi_agent_coordination` | 0 | 0 | 3 | 3 |
| Agent | `structured_decision` | 0 | 0 | 5 | 5 |
| Agent | `tool_selection` | 1 | 0 | 2 | 3 |
| Agent | `tool_trajectory` | 0 | 0 | 5 | 5 |
| Agent | `workflow_design` | 10 | 0 | 4 | 14 |
| Knowledge | `change_control` | 10 | 0 | 0 | 10 |
| Knowledge | `improvement` | 1 | 0 | 4 | 5 |
| Knowledge | `maintenance_engineering` | 0 | 0 | 10 | 10 |
| Knowledge | `manufacturing_execution` | 0 | 0 | 5 | 5 |
| Knowledge | `manufacturing_preparation` | 0 | 1 | 4 | 5 |
| Knowledge | `order` | 0 | 0 | 5 | 5 |
| Knowledge | `procurement` | 0 | 0 | 5 | 5 |
| Knowledge | `production_planning` | 0 | 0 | 5 | 5 |
| Knowledge | `quality` | 0 | 0 | 5 | 5 |
| Knowledge | `shipping` | 1 | 0 | 4 | 5 |
| Reasoning | `5why` | 0 | 0 | 5 | 5 |
| Reasoning | `abnormality_analysis` | 0 | 0 | 5 | 5 |
| Reasoning | `capa` | 1 | 0 | 4 | 5 |
| Reasoning | `data_integrity` | 0 | 0 | 10 | 10 |
| Reasoning | `fmea` | 1 | 0 | 4 | 5 |
| Reasoning | `fta` | 0 | 0 | 5 | 5 |
| Reasoning | `numeric_capacity_planning` | 10 | 0 | 0 | 10 |
| Reasoning | `quality_improvement` | 0 | 0 | 5 | 5 |
| Reasoning | `risk_tradeoff` | 0 | 0 | 10 | 10 |

## 6. English-Only Tasks

Count: 45

```text
IA-HIL-004, IA-HIL-005, IA-HIL-006, IA-HIL-007, IA-HIL-008,
IA-HIL-009, IA-HIL-010, IA-HIL-011, IA-HIL-012, IA-HIL-013,
IA-TS-003, IA-WD-005, IA-WD-006, IA-WD-007, IA-WD-008,
IA-WD-009, IA-WD-010, IA-WD-011, IA-WD-012, IA-WD-013,
IA-WD-014, IK-CC-001, IK-CC-002, IK-CC-003, IK-CC-004,
IK-CC-005, IK-CC-006, IK-CC-007, IK-CC-008, IK-CC-009,
IK-CC-010, IK-IMPR-001, IK-SHIP-004, IR-CAPA-002,
IR-FMEA-001, IR-NCP-001, IR-NCP-002, IR-NCP-003,
IR-NCP-004, IR-NCP-005, IR-NCP-006, IR-NCP-007,
IR-NCP-008, IR-NCP-009, IR-NCP-010
```

## 7. Japanese-Only Tasks

Count: 1

```text
IK-MPREP-005
```

## 8. Mixed-Language Tasks

Count: 134

```text
IA-AD-001, IA-AD-002, IA-AD-003, IA-AD-004,
IA-AS-001, IA-AS-002, IA-AS-003, IA-AS-004, IA-AS-005,
IA-HILB-001, IA-HILB-002, IA-HILB-003, IA-HILB-004, IA-HILB-005,
IA-HIL-001, IA-HIL-002, IA-HIL-003,
IA-MCP-001, IA-MCP-002, IA-MCP-003,
IA-MAC-001, IA-MAC-002, IA-MAC-003,
IA-SD-001, IA-SD-002, IA-SD-003, IA-SD-004, IA-SD-005,
IA-TS-001, IA-TS-002,
IA-TT-001, IA-TT-002, IA-TT-003, IA-TT-004, IA-TT-005,
IA-WD-001, IA-WD-002, IA-WD-003, IA-WD-004,
IK-IMPR-002, IK-IMPR-003, IK-IMPR-004, IK-IMPR-005,
IK-MAINT-001, IK-MAINT-002, IK-MAINT-003, IK-MAINT-004, IK-MAINT-005,
IK-MAINT-006, IK-MAINT-007, IK-MAINT-008, IK-MAINT-009, IK-MAINT-010,
IK-MEXEC-001, IK-MEXEC-002, IK-MEXEC-003, IK-MEXEC-004, IK-MEXEC-005,
IK-MPREP-001, IK-MPREP-002, IK-MPREP-003, IK-MPREP-004,
IK-ORDER-001, IK-ORDER-002, IK-ORDER-003, IK-ORDER-004, IK-ORDER-005,
IK-PROC-001, IK-PROC-002, IK-PROC-003, IK-PROC-004, IK-PROC-005,
IK-PP-001, IK-PP-002, IK-PP-003, IK-PP-004, IK-PP-005,
IK-QUAL-001, IK-QUAL-002, IK-QUAL-003, IK-QUAL-004, IK-QUAL-005,
IK-SHIP-001, IK-SHIP-002, IK-SHIP-003, IK-SHIP-005,
IR-5WHY-001, IR-5WHY-002, IR-5WHY-003, IR-5WHY-004, IR-5WHY-005,
IR-AA-001, IR-AA-002, IR-AA-003, IR-AA-004, IR-AA-005,
IR-CAPA-001, IR-CAPA-003, IR-CAPA-004, IR-CAPA-005,
IR-DI-001, IR-DI-002, IR-DI-003, IR-DI-004, IR-DI-005,
IR-DI-006, IR-DI-007, IR-DI-008, IR-DI-009, IR-DI-010,
IR-FMEA-002, IR-FMEA-003, IR-FMEA-004, IR-FMEA-005,
IR-FTA-001, IR-FTA-002, IR-FTA-003, IR-FTA-004, IR-FTA-005,
IR-QI-001, IR-QI-002, IR-QI-003, IR-QI-004, IR-QI-005,
IR-RT-001, IR-RT-002, IR-RT-003, IR-RT-004, IR-RT-005,
IR-RT-006, IR-RT-007, IR-RT-008, IR-RT-009, IR-RT-010
```

## 9. Examples of Mixed-Language Tasks

| ID | Layer | Category | Reason for mixed classification |
|---|---|---|---|
| `IA-AD-001` | Agent | `agent_design` | Japanese task text with English system terms such as ERP, MES, Excel, JSON, and HITL. |
| `IA-AS-001` | Agent | `agent_safety` | Japanese prompt plus required English JSON fields such as `decision`, `rationale`, `risk_level`, and `required_approvals`. |
| `IA-HILB-001` | Agent | `hil_boundary` | Japanese HIL-boundary task with English control terms, JSON structure, SLA, and audit-log field names. |
| `IK-MAINT-001` | Knowledge | `maintenance_engineering` | Japanese maintenance scenario with English technical identifiers and rubric structure. |
| `IR-DI-001` | Reasoning | `data_integrity` | Japanese data-integrity case with English data-system and validation terminology. |
| `IR-RT-001` | Reasoning | `risk_tradeoff` | Japanese risk-tradeoff prompt with English rubric keys and industrial abbreviations. |

## 10. Observations

- The dataset is best described as multilingual, not English-only or Japanese-only.
- Most mixed records appear to be Japanese task content with English technical terms, field names, IDs, or rubric structure.
- English-only coverage is concentrated in recently added categories such as `change_control`, `numeric_capacity_planning`, later `human_in_the_loop`, and later `workflow_design` items.
- Japanese-only coverage is rare because English structural tokens and rubric keys commonly appear even in Japanese tasks.
- Current dataset-level metadata `language: [en, ja]` is directionally correct, but item-level metadata is needed for precise filtering and evaluation reporting.

## 11. Recommended Normalization Strategy

### Step 1: Metadata-Only Normalization

Add item-level metadata in a future v2.1 or v2.2 schema migration:

| Field | Recommended values |
|---|---|
| `language` | `en`, `ja`, `mixed` |
| `source_language` | `en`, `ja`, `unknown` |
| `translation_role` | `source`, `translation`, `adaptation`, `unpaired` |
| `translation_group_id` | optional; present only for reviewed translation/adaptation groups |

For the current 180-record baseline, initial migration should not translate content. It should assign `language` based on audit results and use `source_language: unknown` where provenance is not reliable.

### Step 2: Human Review of Mixed Records

Review the 134 mixed records and split them into practical subtypes:

- Japanese prompt with English technical terms.
- Japanese prompt with English schema or JSON field requirements.
- English prompt with Japanese domain terms.
- True bilingual content.
- Mojibake or encoding artifact requiring content repair.

The audit label `mixed` should not automatically imply that the item has an English/Japanese translation pair.

### Step 3: Preserve Current Benchmark Identity

Until translation pairs are reviewed, records should default to:

```text
translation_role: unpaired
translation_group_id: omitted
```

This avoids false equivalence between tasks that only appear related by language.

### Step 4: Optional Translation Expansion

After metadata normalization, the project can decide whether to:

- translate selected Japanese or mixed records into English
- translate selected English records into Japanese
- create reviewed source/translation/adaptation groups
- report scores by language and translation group

This should be a separate content migration task, not part of this audit.

## 12. Conclusion

The current 180-task dataset is multilingual in practice because English, Japanese, and mixed-language records coexist.

However, it is not yet language-normalized. The dataset does not yet provide item-level language metadata, source-language provenance, or reviewed translation-group relationships.

The recommended next step is language normalization before public feedback collection or broader multilingual expansion. Translation should come only after metadata classification and human review of task equivalence.
