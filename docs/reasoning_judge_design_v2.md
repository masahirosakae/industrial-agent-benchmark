# Reasoning Judge Design v2.0.0

This document defines the official Rubric Judge architecture for the Industrial Reasoning layer of Industrial Agent Benchmark v2.0.0.

This is a design document only. It does not implement judge code.

## 1. Design Goals

The Industrial Reasoning judge should evaluate whether an answer demonstrates scenario-grounded reasoning, not just keyword recall.

Design goals:

- Evaluate multi-step reasoning against explicit rubrics.
- Reward use of scenario-specific facts, numbers, constraints, and roles.
- Detect critical reasoning failures that would cause unsafe or invalid industrial decisions.
- Support human-readable rubrics first, then structured machine-readable rubrics.
- Allow deterministic sub-checks for numeric or structured components.
- Add LLM Judge support later as an explicit, versioned judge mode.
- Keep judge outputs reproducible enough for later calibration and leaderboard policy.

## 2. Rubric Structure

A reasoning rubric should define:

- task intent
- must-have elements
- nice-to-have elements
- critical failure conditions
- evidence traceability
- expected reasoning qualities
- scoring guidance
- optional deterministic checks

Recommended human-readable structure:

```text
Task intent:
  Explain what reasoning capability the question tests.

Must-have:
  Required elements without which the answer cannot receive a high score.

Nice-to-have:
  Additional elements that improve quality but do not replace must-have elements.

Critical failures:
  Errors that cap or fail the score.

Scoring guidance:
  Description of 0-5 score levels.
```

Future structured rubric fields should map directly from this structure.

## 3. Must-have Elements

Must-have elements are required for a correct or high-scoring answer.

Examples:

- identifies the correct root cause chain
- distinguishes symptom, cause, and countermeasure
- uses scenario-specific numbers or constraints
- prioritizes actions in a defensible order
- identifies affected process, lot, customer, or system boundary
- includes containment before permanent corrective action
- explains why rejected alternatives are weaker

Policy:

- Missing one central must-have should normally cap the score at 3 or below.
- Missing multiple central must-haves should normally cap the score at 2 or below.
- Must-have elements should be specific enough that generic industrial advice does not pass.

## 4. Nice-to-have Elements

Nice-to-have elements distinguish adequate answers from strong answers.

Examples:

- includes validation or verification plan
- mentions owner, timing, or escalation path
- explains tradeoffs and residual risk
- includes monitoring metrics
- identifies assumptions
- suggests documentation or audit evidence
- provides a structured table or decision matrix

Policy:

- Nice-to-have elements should not compensate for missing critical must-have elements.
- Nice-to-have coverage can raise a score from 3 to 4 or from 4 to 5.
- Nice-to-have elements should be domain-specific where possible.

## 5. Critical Failure Conditions

Critical failures are severe reasoning errors that should cap or fail the score.

Examples:

- recommends shipping or releasing product despite unresolved quality hold
- ignores a mandatory approval or regulatory constraint
- treats missing data as evidence of conformance
- performs a root-cause conclusion without containment or evidence
- proposes CAPA without verification of effectiveness
- recommends an FMEA action that does not address the highest-risk failure mode
- uses an invalid unit or numeric result that changes the decision
- gives a generic answer that ignores scenario-specific constraints

Policy:

- A critical failure should cap the score at 1 unless the rubric defines a different cap.
- Critical failure detection must include evidence from the answer.
- Critical failures should be explicit in the rubric and not inferred from vague preferences.

## 6. Evidence Traceability

Evidence Traceability evaluates whether the answer connects:

```text
Observation -> Evidence -> Inference -> Conclusion
```

Definition:

- Observation: what happened or what condition is visible in the scenario.
- Evidence: the specific data, record, measurement, role, document, or constraint that supports the reasoning.
- Inference: the reasoning step that interprets the evidence.
- Conclusion: the final diagnosis, priority, decision, or recommended action.

Evidence Traceability is evaluated separately from whether the final conclusion is correct. An answer can reach a plausible conclusion but still score poorly on traceability if it does not show how scenario evidence supports that conclusion.

Must-have examples:

- cites the specific observation or abnormality being explained
- connects at least one scenario-specific evidence item to each major inference
- distinguishes measured facts from assumptions
- explains why the evidence supports the selected conclusion
- identifies evidence gaps when the scenario is insufficient for a final conclusion

Nice-to-have examples:

- presents an observation/evidence/inference/conclusion table
- cites multiple independent evidence sources
- identifies conflicting evidence
- describes what additional evidence would confirm or reject the inference
- ranks conclusions by evidence strength

Critical failure examples:

- states a final root cause with no supporting evidence
- treats missing data as proof of conformance
- invents evidence not present in the scenario
- ignores evidence that contradicts the conclusion
- confuses observation with root cause
- jumps from correlation to conclusion without explaining the inference

## 7. LLM Judge Design

The LLM Judge is a future extension for Industrial Reasoning. It should not replace the rubric; it should apply the rubric.

LLM Judge inputs:

- question ID
- question text
- context
- reference answer
- rubric
- model prediction
- deterministic check results when available

LLM Judge outputs:

- score `0..5`
- must-have assessment
- nice-to-have assessment
- critical failure assessment
- evidence traceability assessment
- evidence snippets
- short judge rationale
- judge model and prompt version metadata

Design constraints:

- LLM Judge usage must be explicit and versioned.
- Prompts must instruct the judge to use only public benchmark content and the submitted prediction.
- The judge must not call external tools unless a later architecture explicitly allows it.
- The judge must produce structured JSON.
- The judge must evaluate evidence traceability separately from conclusion quality.
- The judge should not give full reasoning credit to an answer that reaches the right conclusion through unsupported or invented evidence.
- Judge prompts and output schema must be stable before leaderboard use.

## 8. Result Schema

Reasoning judge results should use the common v2 result format with reasoning-specific metadata:

```json
{
  "id": "IR-CAPA-001",
  "model_id": "sample_model",
  "score": 3,
  "score_method": "rubric_judge_v1",
  "prediction": "...",
  "reference_answer": "...",
  "rubric": "...",
  "metadata": {
    "judge_type": "rubric",
    "judge_version": "2.0.0",
    "must_have_results": [],
    "nice_to_have_results": [],
    "critical_failure_triggered": false,
    "critical_failure_reasons": [],
    "reasoning_quality": "partial",
    "evidence_traceability": {
      "score": 3,
      "observation_supported": true,
      "evidence_supported": true,
      "inference_supported": false,
      "conclusion_supported": true,
      "notes": "Conclusion is plausible, but the inference chain omits one evidence step."
    },
    "deterministic_checks": []
  }
}
```

Required metadata concepts:

- `judge_type`
- `judge_version`
- `must_have_results`
- `nice_to_have_results`
- `critical_failure_triggered`
- `critical_failure_reasons`
- `reasoning_quality`
- `evidence_traceability`

Optional metadata concepts:

- `deterministic_checks`
- `numeric_check_results`
- `structured_output_results`
- `judge_prompt_version`
- `judge_model`

## 9. Scoring Rules

All Industrial Reasoning scores use the 0-5 scale.

| Score | Meaning |
|---:|---|
| 0 | Missing, empty, or irrelevant answer. |
| 1 | Critical failure or fundamentally invalid reasoning. |
| 2 | Major must-have elements missing; weak scenario grounding. |
| 3 | Plausible reasoning with important gaps. |
| 4 | Strong reasoning with minor omissions. |
| 5 | Complete, scenario-specific, well-justified reasoning. |

Scoring policy:

1. Check critical failures first.
2. Apply score caps from critical failures or missing central must-haves.
3. Evaluate must-have elements.
4. Evaluate nice-to-have elements.
5. Evaluate evidence traceability.
6. Evaluate reasoning coherence and scenario specificity.
7. Apply deterministic numeric or structural checks where defined.
8. Produce final score and evidence.

Suggested caps:

| Condition | Maximum score |
|---|---:|
| Empty answer | 0 |
| Critical failure | 1 |
| Central must-have missing | 2 |
| Multiple must-haves missing | 2 |
| Numeric result changes decision and is wrong | 2 |
| Generic answer ignores scenario constraints | 2 |
| Correct conclusion but unsupported evidence chain | 3 |
| Good conclusion but weak reasoning | 3 |

## 10. Example Tasks

### Root Cause Analysis

Capability tested:

- distinguishes symptom from cause
- constructs evidence-based cause chain
- avoids premature conclusion
- supports conclusions with explicit observation-to-evidence-to-inference traceability

Must-have examples:

- identifies observed defect or abnormality
- cites the evidence supporting each major causal inference
- identifies plausible causal chain
- separates containment from root-cause verification
- proposes evidence to confirm or reject causes
- avoids presenting an unsupported conclusion as final

Critical failure examples:

- declares final root cause without evidence
- invents supporting evidence not present in the scenario
- ignores contradictory evidence
- skips containment when product risk remains

### FMEA

Capability tested:

- prioritizes failure modes and controls
- reasons about severity, occurrence, and detection
- proposes action against highest-risk items

Must-have examples:

- identifies failure mode, effect, and cause
- prioritizes by risk
- proposes control or action tied to the risk driver

Critical failure examples:

- treats low-risk cosmetic issues as higher priority than safety or shipment-critical issues
- proposes action that does not address the failure mode

### CAPA

Capability tested:

- designs corrective and preventive actions
- includes containment, root cause, corrective action, verification, and prevention

Must-have examples:

- immediate containment
- root cause verification
- corrective action
- effectiveness check
- prevention or systemic action

Critical failure examples:

- closes CAPA without effectiveness verification
- confuses correction with corrective action

### Quality Improvement

Capability tested:

- selects improvement actions from process evidence
- links metrics, countermeasures, and monitoring

Must-have examples:

- uses provided process data
- identifies improvement priority
- proposes measurable countermeasure
- defines monitoring metric

Critical failure examples:

- recommends broad training only when process evidence points to equipment or method failure
- ignores customer or safety impact

### Numeric Capacity Planning

Capability tested:

- performs capacity, takt, OEE, workload, staffing, or equipment-count reasoning
- applies constraints and units correctly

Must-have examples:

- calculates required time, capacity, or resource count
- uses correct unit conversion
- applies bottleneck or availability constraint
- explains rounding or feasibility decision

Critical failure examples:

- uses an invalid unit that changes the decision
- fails to round required equipment or staffing up when partial resources are impossible
- ignores legal or operational constraints on overtime or capacity

## 11. Roadmap

### Phase 1: Human-readable rubric

Define clear written rubrics for each reasoning task.

Deliverables:

- must-have elements
- nice-to-have elements
- critical failures
- score guidance

### Phase 2: Structured rubric schema

Convert human-readable rubrics into machine-readable schema.

Deliverables:

- structured must-have objects
- structured nice-to-have objects
- structured critical failure objects
- deterministic check references

### Phase 3: LLM Judge integration

Add an explicit LLM Judge mode for rubric application.

Deliverables:

- judge prompt template
- structured judge output schema
- prompt versioning
- reproducibility metadata

### Phase 4: Judge calibration

Calibrate judge behavior before any leaderboard use.

Deliverables:

- calibration set
- inter-judge agreement review
- score distribution review
- failure-mode audit
- versioned judge release notes

## Non-Goals

This document does not implement judge code, modify benchmark questions, add new dataset records, or create leaderboard behavior.
