# Knowledge Judge Design v2.0.0

This document defines the official Deterministic Judge design for the Industrial Knowledge layer of Industrial Agent Benchmark v2.0.0.

This is a design document only. It does not implement judge code and does not modify benchmark questions.

## 1. Design Goals

The Industrial Knowledge judge must be:

- Reproducible
- Deterministic
- Cheap to execute
- Independent of external APIs
- Independent of LLM judges

The judge should evaluate facts, terminology, numeric calculations, checklist coverage, and structured fields using explicit public rules.

## 2. Supported Judge Types

### A. Exact Match

Exact Match checks whether an answer contains the required literal value or phrase.

Use cases:

- terminology
- standards
- abbreviations
- exact labels
- required categorical decisions

Examples:

- `IATF 16949`
- `ISO 13485`
- `PPAP`
- `CAPA`
- `quality hold`

Exact Match is appropriate when wording variation should not be accepted or when the benchmark item explicitly asks for a specific term.

### B. Canonical Match

Canonical Match checks whether an answer maps to an accepted canonical concept even if the wording differs.

Use cases:

- abbreviation expansion
- accepted synonyms
- equivalent operational phrases
- normalized terminology

Examples:

| Canonical value | Accepted aliases |
|---|---|
| `CAPA` | `Corrective and Preventive Action` |
| `PCN` | `Process Change Notification`, `Product Change Notification` |
| `PPAP` | `Production Part Approval Process` |
| `quality hold` | `shipment hold`, `release block`, `quarantine hold` |

Canonical Match is appropriate when industrial users may express the same concept in multiple accepted forms.

### C. Numeric Match

Numeric Match checks whether an answer contains a required numeric result.

Use cases:

- takt time
- OEE
- availability
- capacity calculations
- payback period
- defect rate
- required equipment count

Supported behavior:

- tolerance
- unit normalization
- integer rounding requirements
- percent and decimal normalization
- exact-match mode for count values

Examples:

| Check | Expected | Tolerance |
|---|---:|---|
| takt time | `45.0 sec/unit` | `+/- 0.5 sec` |
| OEE | `0.72` or `72%` | `+/- 0.01` |
| required machines | `3` | exact |
| missing inspection rate | `10%` | `+/- 0.1 percentage point` |

Numeric Match should fail when the number is correct but the unit is invalid for the scenario.

### D. Checklist Match

Checklist Match checks whether required and optional elements are present.

Use cases:

- change control procedures
- quality hold release requirements
- maintenance planning steps
- shipment readiness gates
- compliance document sets

Supported behavior:

- required elements
- optional elements
- critical missing elements
- aliases for checklist items
- minimum required count

Examples of required elements for a quality hold release question:

- identify the hold condition
- verify inspection completion
- require authorized quality approval
- prevent shipment before release
- record audit evidence

Optional elements may improve the score but cannot compensate for a critical missing approval or unsafe release decision.

### E. Structured Field Match

Structured Field Match checks whether an answer follows a required structure and contains required fields.

Use cases:

- JSON outputs
- YAML outputs
- table outputs
- structured approval plans
- checklist tables

Supported behavior:

- parse JSON or YAML when required
- validate required field names
- validate allowed values
- validate field type
- validate non-empty field content
- validate required table columns

Examples:

- JSON field `decision` must be `hold` or `do_not_release`
- JSON field `required_approval` must mention quality approval
- table columns must include `risk`, `owner`, and `action`

Structured Field Match should fail clearly when output is unparseable or required fields are missing.

## 3. Judge Schema

Each deterministic judge rule should use a common schema:

```json
{
  "judge_type": "checklist_match",
  "max_score": 5,
  "required_elements": [],
  "optional_elements": [],
  "numeric_constraints": [],
  "allowed_aliases": []
}
```

Recommended expanded fields:

```json
{
  "judge_type": "numeric_match",
  "max_score": 5,
  "required_elements": [
    {
      "id": "requires_quality_approval",
      "description": "Answer states that quality approval is required before release",
      "weight": 1
    }
  ],
  "optional_elements": [
    {
      "id": "mentions_audit_log",
      "description": "Answer mentions audit log or evidence record",
      "weight": 1
    }
  ],
  "numeric_constraints": [
    {
      "id": "oee",
      "expected_value": 0.72,
      "unit": "ratio",
      "tolerance": 0.01,
      "required": true
    }
  ],
  "allowed_aliases": [
    {
      "canonical": "CAPA",
      "aliases": [
        "Corrective and Preventive Action"
      ]
    }
  ]
}
```

Allowed `judge_type` values:

- `exact_match`
- `canonical_match`
- `numeric_match`
- `checklist_match`
- `structured_field_match`

## 4. Scoring Rules

All Industrial Knowledge judge scores use the 0-5 scale.

Recommended scoring:

| Score | Meaning |
|---:|---|
| 0 | Missing, empty, or unparseable answer. |
| 1 | Critical failure or unsafe knowledge claim. |
| 2 | Major required elements missing. |
| 3 | Most required elements present, but important gaps remain. |
| 4 | All required elements present, with minor optional gaps. |
| 5 | All required elements present, strong optional coverage, no deterministic failures. |

Calculation policy:

1. Start with `max_score`.
2. Apply critical failure rules first.
3. If a critical failure is triggered, cap the score at `1`.
4. Subtract or cap for missing required elements.
5. Add optional element credit only after required elements pass.
6. Apply numeric and unit failures as required-element failures.
7. Apply structured-output failures before optional credit.
8. Clamp final score to `0..max_score`.

Suggested caps:

| Condition | Maximum score |
|---|---:|
| Empty answer | 0 |
| Unsafe release decision | 1 |
| Mandatory approval missing | 2 |
| Required numeric result missing | 3 |
| Required unit invalid | 3 |
| Required structured field missing | 3 |
| Required checklist element missing | 4 |

## 5. Failure Conditions

Failure conditions should be explicit, public, and deterministic.

Examples:

- unsafe release decision
- missing mandatory approval
- invalid unit
- wrong standard or abbreviation
- numeric value outside tolerance
- required checklist step absent
- unparseable required JSON/YAML
- required structured field missing
- answer contradicts the hold or escalation requirement

Critical failures should be rare and reserved for answers that would create unsafe or invalid industrial action.

## 6. Example Questions

### Quality

Question type: quality hold release requirement.

Expected deterministic checks:

- exact or canonical match for `quality hold`
- checklist match for inspection completion
- checklist match for authorized quality approval
- failure condition for shipment release before approval
- optional element for audit evidence

Recommended judge types:

- `canonical_match`
- `checklist_match`
- `structured_field_match` if JSON is required

### Maintenance

Question type: maintenance cost-benefit or equipment availability.

Expected deterministic checks:

- numeric match for annual failure cost
- numeric match for downtime or availability
- numeric match for payback period
- unit normalization for currency, hours, percent, or years
- checklist match for implementation constraints

Recommended judge types:

- `numeric_match`
- `checklist_match`

### Production Planning

Question type: capacity, takt, equipment count, or production feasibility.

Expected deterministic checks:

- numeric match for takt time
- numeric match for required equipment count
- exact integer match for headcount or machine count
- unit normalization for seconds, minutes, hours, and percent utilization
- failure condition for ignoring bottleneck or capacity constraint

Recommended judge types:

- `numeric_match`
- `structured_field_match` for required calculation tables

### Change Control

Question type: process change, customer approval, PCN/ECN, or PPAP requirement.

Expected deterministic checks:

- canonical match for PCN, ECN, PPAP, or 4M change
- checklist match for impact assessment
- checklist match for customer or quality approval
- checklist match for traceability boundary
- failure condition for implementing the change before required approval

Recommended judge types:

- `canonical_match`
- `checklist_match`
- `structured_field_match`

## 7. Implementation Roadmap

### Phase 1: Exact Match

Implement:

- literal phrase checks
- case-insensitive matching
- whitespace normalization
- pass/fail evidence reporting

Primary use:

- terminology
- standards
- abbreviations

### Phase 2: Numeric Match

Implement:

- number extraction
- tolerance checks
- unit normalization
- percent/decimal normalization
- exact integer checks

Primary use:

- takt time
- OEE
- capacity calculations
- maintenance calculations

### Phase 3: Checklist Match

Implement:

- required element matching
- optional element matching
- aliases per checklist item
- score caps for missing mandatory elements
- critical failure detection

Primary use:

- quality gates
- change control procedures
- maintenance planning
- shipment readiness

### Phase 4: Structured Output Match

Implement:

- JSON parsing
- YAML parsing
- table column validation
- required field checks
- allowed value checks
- type checks

Primary use:

- structured decisions
- approval plans
- calculation tables
- audit-ready outputs

## Non-Goals

This design does not implement code, modify benchmark questions, add new dataset records, or define leaderboard behavior.
