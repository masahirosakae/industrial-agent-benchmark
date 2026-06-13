# Evaluation Architecture v2.0.0

This document defines the official evaluation architecture for Industrial Agent Benchmark v2.0.0.

## 1. Design Principles

The v2.0.0 evaluation architecture separates dataset publication, answer generation, judging, summarization, and leaderboard publication.

Core principles:

- Public benchmark data is separate from generated evaluation outputs.
- Evaluation stages must be reproducible and versioned.
- Judge type must match the capability being measured.
- Simple deterministic pipelines should exist before more complex judging is added.
- External APIs and LLM judges must be explicit, optional, and versioned.
- Generated outputs under `results/` are local artifacts and are not committed.
- Leaderboard support is a later layer, not part of the core dataset or first judge implementation.

## 2. Layer Definitions

### Industrial Knowledge

Industrial Knowledge evaluates whether a system can apply manufacturing domain facts, procedures, constraints, terminology, and standard operational knowledge.

Examples:

- quality hold requirements
- maintenance planning
- production and shipment constraints
- change-control procedures
- compliance process knowledge

Official judge type: Deterministic Judge.

Rationale: Knowledge questions should be structured so that required facts, numeric values, units, categories, or checklist elements can be evaluated deterministically whenever possible.

### Industrial Reasoning

Industrial Reasoning evaluates multi-step reasoning over industrial scenarios.

Examples:

- root-cause analysis
- risk tradeoff decisions
- data-integrity assessment
- numeric capacity planning
- prioritization under constraints

Official judge type: Rubric Judge plus LLM Judge.

Rationale: Reasoning answers often require qualitative assessment against a rubric. Deterministic checks can validate numeric or structural components, but final reasoning quality may require rubric-based judgement.

### Industrial Agent

Industrial Agent evaluates whether a system can behave safely and correctly as an agent in industrial workflows.

Examples:

- human-in-the-loop boundaries
- tool trajectory planning
- blocked actions before approval
- audit logging
- escalation paths
- safe deferral

Official judge type: Executable Judge.

Rationale: Agent questions should eventually be evaluated by executable scenarios, state machines, tool-call traces, mocks, or sandboxed workflows rather than by text-only judgement alone.

## 3. Judge Types

### Deterministic Judge

A Deterministic Judge evaluates answers using explicit rules and reproducible checks.

Typical checks:

- exact or tolerance-based numeric checks
- required keyword or field presence
- schema validation
- multiple-choice answer match
- unit consistency
- required checklist coverage

Current status: partially implemented as a deterministic rule-based pipeline for v2 judgement file generation. The current token-overlap scorer is a placeholder for pipeline validation, not the final knowledge judge.

### Rubric Judge

A Rubric Judge evaluates answers against written criteria.

Typical checks:

- must-have coverage
- nice-to-have coverage
- critical failure detection
- reasoning coherence
- scenario-specific constraint use
- structured decision quality

Rubric judging may combine deterministic checks with human or LLM-assisted judgement.

### Executable Judge

An Executable Judge evaluates behavior through executable scenarios.

Typical checks:

- tool-call sequence validity
- forbidden action blocking
- approval state transitions
- final state correctness
- audit log completeness
- recovery from missing or conflicting data

Executable judges should use mocks, fixtures, or sandboxed environments. They should not require production systems or private credentials.

## 4. Score Definitions

All scores use a 0-5 scale in v2.0.0.

### Knowledge Score

Knowledge Score measures factual and procedural correctness.

Interpretation:

- `0`: no answer or unusable answer
- `1`: mostly incorrect or unsafe factual claim
- `2`: partial but missing core required elements
- `3`: mostly correct with gaps or weak specificity
- `4`: correct and specific, with minor omissions
- `5`: complete, precise, and aligned with the public reference/rubric

Primary judge: Deterministic Judge.

### Reasoning Score

Reasoning Score measures scenario-grounded industrial reasoning.

Interpretation:

- `0`: no answer or irrelevant answer
- `1`: reasoning fails the central scenario constraint
- `2`: partial reasoning with major missing steps
- `3`: plausible reasoning with incomplete tradeoff analysis
- `4`: strong reasoning with minor gaps
- `5`: complete, scenario-specific, well-justified reasoning

Primary judge: Rubric Judge plus LLM Judge. Deterministic sub-checks may support numeric or structural requirements.

### Agent Score

Agent Score measures safe and effective agent behavior.

Interpretation:

- `0`: no executable plan or no meaningful answer
- `1`: unsafe or forbidden action
- `2`: major boundary, state, or tool-use gaps
- `3`: plausible agent behavior with incomplete safeguards
- `4`: safe behavior with minor trace or escalation gaps
- `5`: correct tool/state trajectory with appropriate human approval and audit behavior

Primary judge: Executable Judge.

## 5. Result Schema

### Common Result Format

All judge outputs should share a common top-level structure:

```json
{
  "id": "IA-HILB-001",
  "model_id": "sample_model",
  "score": 2,
  "score_method": "rule_based_token_overlap_v1",
  "prediction": "...",
  "reference_answer": "...",
  "rubric": "...",
  "metadata": {}
}
```

Required fields:

- `id`
- `model_id`
- `score`
- `score_method`
- `prediction`
- `reference_answer`
- `rubric`
- `metadata`

### Common Metadata Fields

Recommended metadata fields:

- `judge_type`
- `judge_version`
- `dataset_version`
- `score_method`
- `reason`
- `checks_passed`
- `checks_failed`
- `critical_failure_triggered`
- `missing_required_elements`
- `numeric_check_results`
- `structured_output_results`
- `execution_trace_summary`

Metadata may vary by judge type, but it must remain JSON-serializable and public-safe.

## 6. Judge Roadmap

### Current Implementation

Current v2.0.0 implementation:

- simple evaluation prepares standardized prediction JSONL files
- deterministic judge evaluation writes `judgements.jsonl`
- current scoring method is `rule_based_token_overlap_v1`
- no external APIs
- no LLM judge
- no executable environment
- no leaderboard implementation

The current judge is a pipeline and file-format implementation, not the final benchmark judge.

### Future Implementation

Planned future direction:

1. Replace placeholder token-overlap scoring for Industrial Knowledge with deterministic field, keyword, numeric, and schema checks.
2. Add Rubric Judge support for Industrial Reasoning, including explicit must-have and critical-failure evaluation.
3. Add optional LLM Judge support for reasoning-quality assessment, with versioned prompts and reproducibility metadata.
4. Add Executable Judge support for Industrial Agent tasks using mocks, tool traces, state machines, or sandbox fixtures.
5. Add score aggregation after individual judge types are stable.
6. Add leaderboard workflow only after judging behavior is stable and documented.

## 7. Leaderboard Implications

Leaderboard entries must identify:

- dataset version
- judge type
- judge version
- score method
- split
- run date
- public display name

Leaderboard scores should not combine incompatible judge versions. A result produced by the placeholder deterministic scorer is not comparable to a future rubric or executable judge unless explicitly marked as such.

No leaderboard implementation is included in this architecture document.

## 8. Backward Compatibility

v1.1.0 remains a frozen pre-release benchmark snapshot. v2.0.0 introduces a cleaner dataset schema and staged evaluation architecture.

Compatibility policy:

- v1.1.0 public question IDs should be preserved where migrated.
- v1.1.0 public reference answers and rubrics may be transformed into v2 schema fields.
- v1.1.0 non-public run context must not be migrated.
- v2 result files should use the common result schema even when judge internals evolve.
- Future judge changes must version `score_method` and `judge_version` so old results remain interpretable.
