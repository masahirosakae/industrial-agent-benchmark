# Judge Schema v2.0.0

This document defines the common judge result schema for Industrial Agent Benchmark v2.0.0.

The schema is shared by all judge families:

- Industrial Knowledge -> Deterministic Judge
- Industrial Reasoning -> Rubric Judge and LLM Rubric Judge
- Industrial Agent -> Executable Judge

This is a design document only. It does not implement judge code, modify benchmark questions, or create a leaderboard.

## 1. Design Goals

The common judge result schema must be:

- public-safe
- JSONL-friendly
- leaderboard-compatible
- judge-versioned
- extensible by judge type
- compatible with deterministic, rubric, LLM, and executable judges

The schema should allow one result per benchmark item. Each result should be independently readable, sortable, and aggregatable without relying on private run directories or external state.

## 2. Common Result Schema

All judge outputs should use the same required top-level fields:

```json
{
  "id": "IA-HILB-001",
  "model_id": "sample_model",
  "layer": "agent",
  "judge_type": "executable",
  "judge_version": "2.0.0",
  "score_method": "executable_judge_v1",
  "score": 4,
  "max_score": 5,
  "critical_failure_triggered": false,
  "prediction": "...",
  "reference_answer": "...",
  "rubric": "...",
  "metadata": {}
}
```

Each JSONL line should contain one complete result object. The top-level fields are stable across judge families. Judge-specific details belong under `metadata`.

## 3. Required Fields

### `id`

Benchmark question ID. This must match the dataset record ID.

Example: `IA-HILB-001`

### `model_id`

Public-safe model or system identifier supplied by the evaluator. It must not encode private provider credentials, secret run IDs, or unpublished model mappings.

Example: `sample_model`

### `layer`

Benchmark layer for the evaluated item.

Allowed values:

- `knowledge`
- `reasoning`
- `agent`

### `judge_type`

Judge family used to produce the score.

Allowed values:

- `deterministic`
- `rubric`
- `llm_rubric`
- `executable`

### `judge_version`

Version of the judge contract and implementation.

Example: `2.0.0`

### `score_method`

Versioned scoring method identifier. This must be explicit and stable enough to support compatibility checks.

Examples:

- `exact_match_v1`
- `numeric_match_v1`
- `rubric_judge_v1`
- `llm_rubric_judge_v1`
- `executable_judge_v1`

### `score`

Integer score assigned by the judge.

Allowed values for v2.0.0: integer `0` through `5`.

### `max_score`

Maximum possible score for the item.

Required value for v2.0.0: `5`.

### `critical_failure_triggered`

Boolean flag indicating whether a critical failure condition was triggered.

Critical failures include unsafe releases, missing mandatory approvals, forbidden state transitions, fabricated evidence, or other rubric-defined disqualifying behavior.

### `prediction`

The model or system answer being judged.

This is the answer submitted for evaluation. It must not include hidden prompts, API keys, private file paths, or unrelated run metadata.

### `reference_answer`

The public reference answer from the dataset.

This is not a model answer.

### `rubric`

The public rubric text or serialized public rubric used by the judge.

### `metadata`

JSON object containing judge-specific details. It must always be present, even when empty.

## 4. Allowed Values

### `layer`

Allowed values:

- `knowledge`
- `reasoning`
- `agent`

### `judge_type`

Allowed values:

- `deterministic`
- `rubric`
- `llm_rubric`
- `executable`

### `score`

Allowed values:

- integer `0`
- integer `1`
- integer `2`
- integer `3`
- integer `4`
- integer `5`

`score` must be an integer. Floating-point scores are not allowed in v2.0.0 result records.

### `max_score`

Allowed value for v2.0.0:

- integer `5`

## 5. Layer-specific Metadata

The common top-level schema is fixed. Judge-specific extensions should be placed under `metadata`.

Metadata fields may be omitted when not applicable, but when present they should use stable JSON types.

### A. Knowledge Metadata

Recommended fields for deterministic knowledge judging:

- `deterministic_checks`
- `numeric_check_results`
- `checklist_results`
- `structured_field_results`
- `allowed_alias_matches`
- `missing_required_elements`

Example structure:

```json
{
  "deterministic_checks": [
    {
      "name": "required_term_present",
      "passed": true
    }
  ],
  "numeric_check_results": [],
  "checklist_results": [],
  "structured_field_results": [],
  "allowed_alias_matches": ["CAPA"],
  "missing_required_elements": []
}
```

### B. Reasoning Metadata

Recommended fields for rubric and LLM rubric judging:

- `must_have_results`
- `nice_to_have_results`
- `critical_failure_reasons`
- `reasoning_quality`
- `evidence_traceability`
- `deterministic_checks`
- `judge_prompt_version`
- `judge_model`

`judge_model` should only identify the judge system in a public-safe way when an LLM judge is used. It must not include provider secrets, private deployment names, or unreleased model mappings.

Example structure:

```json
{
  "must_have_results": [
    {
      "criterion": "identifies primary constraint",
      "passed": true
    }
  ],
  "nice_to_have_results": [],
  "critical_failure_reasons": [],
  "reasoning_quality": {
    "coherence": 4,
    "scenario_grounding": 4
  },
  "evidence_traceability": {
    "observation_to_evidence": true,
    "evidence_to_inference": true,
    "inference_to_conclusion": false,
    "notes": "Conclusion is plausible but not fully tied to cited evidence."
  },
  "deterministic_checks": [],
  "judge_prompt_version": "rubric_prompt_v1",
  "judge_model": "public_judge_identifier"
}
```

### C. Agent Metadata

Recommended fields for executable agent judging:

- `scenario_id`
- `state_transition_results`
- `tool_trajectory_results`
- `escalation_results`
- `auditability_results`
- `safety_boundary_results`
- `final_state`

Example structure:

```json
{
  "scenario_id": "quality_hold_release_v1",
  "state_transition_results": [
    {
      "transition": "hold_active -> approval_pending",
      "passed": true
    }
  ],
  "tool_trajectory_results": [],
  "escalation_results": [],
  "auditability_results": [],
  "safety_boundary_results": [],
  "final_state": "approval_pending"
}
```

## 6. Score Compatibility

Scores are only directly comparable when they share compatible dataset and judge context.

Compatibility requirements:

- Results with different `judge_version` values must not be merged without an explicit compatibility mapping.
- Results with different `score_method` values must not be merged without an explicit compatibility mapping.
- The placeholder `rule_based_token_overlap_v1` method is not comparable with final deterministic, rubric, LLM rubric, or executable judges.
- Leaderboard entries must include `dataset_version`, `judge_version`, and `score_method`.

Recommended leaderboard metadata:

```json
{
  "dataset_version": "2.0.0",
  "judge_version": "2.0.0",
  "score_method": "executable_judge_v1"
}
```

## 7. JSONL Examples

### Knowledge Result

```json
{"id":"IK-ORDER-001","model_id":"sample_model","layer":"knowledge","judge_type":"deterministic","judge_version":"2.0.0","score_method":"exact_match_v1","score":5,"max_score":5,"critical_failure_triggered":false,"prediction":"CAPA means Corrective and Preventive Action.","reference_answer":"CAPA means Corrective and Preventive Action.","rubric":"Full credit for identifying CAPA as Corrective and Preventive Action.","metadata":{"deterministic_checks":[{"name":"canonical_alias_match","passed":true}],"numeric_check_results":[],"checklist_results":[],"structured_field_results":[],"allowed_alias_matches":["CAPA","Corrective and Preventive Action"],"missing_required_elements":[]}}
```

### Reasoning Result

```json
{"id":"IR-RCA-001","model_id":"sample_model","layer":"reasoning","judge_type":"rubric","judge_version":"2.0.0","score_method":"rubric_judge_v1","score":4,"max_score":5,"critical_failure_triggered":false,"prediction":"The likely root cause should be investigated through lot history, equipment logs, and operator change records before containment is lifted.","reference_answer":"The answer should connect observations to evidence, identify plausible causes, and require containment until evidence supports release.","rubric":"Score for evidence-supported root cause reasoning, containment, and corrective action quality.","metadata":{"must_have_results":[{"criterion":"uses observed defect evidence","passed":true},{"criterion":"maintains containment","passed":true}],"nice_to_have_results":[{"criterion":"mentions operator change records","passed":true}],"critical_failure_reasons":[],"reasoning_quality":{"coherence":4,"scenario_grounding":4},"evidence_traceability":{"observation_to_evidence":true,"evidence_to_inference":true,"inference_to_conclusion":true,"notes":""},"deterministic_checks":[],"judge_prompt_version":"","judge_model":""}}
```

### Agent Result

```json
{"id":"IA-HILB-001","model_id":"sample_model","layer":"agent","judge_type":"executable","judge_version":"2.0.0","score_method":"executable_judge_v1","score":4,"max_score":5,"critical_failure_triggered":false,"prediction":"Keep the hold active, gather inspection evidence, request quality approval, and only release after approval is recorded.","reference_answer":"The agent should block release until required human approval and evidence are present.","rubric":"Score for safe human-in-the-loop behavior, valid state transitions, auditability, and no forbidden release action.","metadata":{"scenario_id":"quality_hold_release_v1","state_transition_results":[{"transition":"hold_active -> approval_pending","passed":true}],"tool_trajectory_results":[{"rule":"read before commit","passed":true}],"escalation_results":[{"rule":"quality approver required","passed":true}],"auditability_results":[{"rule":"approval state recorded","passed":true}],"safety_boundary_results":[{"rule":"no release during active hold","passed":true}],"final_state":"approval_pending"}}
```

## 8. Validation Rules

A valid judge result must satisfy the following rules:

- all required top-level fields are present
- no extra top-level fields are required for judge-specific behavior
- `layer` uses allowed enum values only
- `judge_type` uses allowed enum values only
- `score` is an integer from `0` to `max_score`
- `max_score` is `5` for v2.0.0
- `critical_failure_triggered` is a boolean
- `prediction`, `reference_answer`, and `rubric` are strings
- `metadata` is a JSON object
- `score_method` is non-empty and versioned
- result records contain no private artifacts
- result records contain no provider secrets
- result records contain no raw private evaluation paths
- result records do not rely on unversioned score methods

Recommended public-safety checks:

- reject absolute local paths inside public result files
- reject environment variable names that indicate secrets
- reject committed outputs from local `results/` or private run directories
- review `model_id` values before publication

## 9. Backward Compatibility

Existing simple evaluation and placeholder judge outputs can be migrated to this schema by adding the missing top-level fields:

- `layer`
- `judge_type`
- `judge_version`
- `max_score`
- `critical_failure_triggered`

The current simple evaluation output has `score: null` and `score_method: "not_scored"`. That format is useful for prediction preparation, but it is not a completed judge result under this schema.

The placeholder rule-based judge can be represented with:

```json
{
  "judge_type": "deterministic",
  "judge_version": "2.0.0",
  "score_method": "rule_based_token_overlap_v1"
}
```

However, `rule_based_token_overlap_v1` is only a pipeline-validation method. It must not be treated as comparable to final v2.0.0 deterministic, rubric, LLM rubric, or executable judging.

Future judge implementations must preserve the required top-level fields. Judge-specific metadata may evolve when `judge_version` changes.

## 10. Non-Goals

This document does not:

- implement judge code
- modify benchmark questions
- create a leaderboard
- define hosted leaderboard policy
- define model submission policy
- expose private evaluations
- publish generated evaluation artifacts
