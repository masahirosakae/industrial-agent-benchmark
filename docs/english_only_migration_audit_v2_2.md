# English-only Migration Audit v2.2

This document audits the English-only benchmark records and prepares their migration into Japanese canonical records.

It is an audit and planning document only. It does not translate tasks, modify benchmark content, update JSONL files, or change exporter, validator, schema, or evaluation code.

## 1. Background

Project language policy:

- canonical language: Japanese
- English records are translated or derivative distributions
- v2.0.1 remains immutable
- historical artifacts must not be silently mutated

Current language audit:

| Language class | Count |
|---|---:|
| English-only | 45 |
| Japanese-only | 1 |
| Mixed-language | 134 |
| Total | 180 |

The 45 English-only records are the primary blocker to a Japanese-canonical benchmark.

## 2. Inventory

| ID | Layer | Category | Sub-category | Title or short description |
|---|---|---|---|---|
| `IA-HIL-004` | Agent | agent | `human_in_the_loop` | Quality Hold Release Approval Boundary |
| `IA-HIL-005` | Agent | agent | `human_in_the_loop` | Engineering Change Implementation Approval |
| `IA-HIL-006` | Agent | agent | `human_in_the_loop` | Customer Approval Before Shipment |
| `IA-HIL-007` | Agent | agent | `human_in_the_loop` | CAPA Closure Requires Effectiveness Approval |
| `IA-HIL-008` | Agent | agent | `human_in_the_loop` | Maintenance Work Authorization Boundary |
| `IA-HIL-009` | Agent | agent | `human_in_the_loop` | Overtime Schedule Commitment Approval |
| `IA-HIL-010` | Agent | agent | `human_in_the_loop` | Supplier Deviation Approval Boundary |
| `IA-HIL-011` | Agent | agent | `human_in_the_loop` | Conflicting Approval State Escalation |
| `IA-HIL-012` | Agent | agent | `human_in_the_loop` | Automated Document Release Boundary |
| `IA-HIL-013` | Agent | agent | `human_in_the_loop` | Emergency Stop-Ship Escalation |
| `IA-TS-003` | Agent | agent | `tool_selection` | Tool Selection for Noisy Line Handover Support |
| `IA-WD-005` | Agent | agent | `workflow_design` | Quality Issue Investigation Workflow |
| `IA-WD-006` | Agent | agent | `workflow_design` | Engineering Change Workflow |
| `IA-WD-007` | Agent | agent | `workflow_design` | Nonconforming Material Disposition Workflow |
| `IA-WD-008` | Agent | agent | `workflow_design` | Production Recovery Workflow |
| `IA-WD-009` | Agent | agent | `workflow_design` | Supplier Deviation Workflow |
| `IA-WD-010` | Agent | agent | `workflow_design` | Maintenance Escalation Workflow |
| `IA-WD-011` | Agent | agent | `workflow_design` | Inspection Plan Update Workflow |
| `IA-WD-012` | Agent | agent | `workflow_design` | Customer Complaint Response Workflow |
| `IA-WD-013` | Agent | agent | `workflow_design` | Containment and Release Workflow |
| `IA-WD-014` | Agent | agent | `workflow_design` | Audit-ready Workflow Documentation |
| `IK-CC-001` | Knowledge | knowledge | `change_control` | Required Change Request Fields |
| `IK-CC-002` | Knowledge | knowledge | `change_control` | Change Approval Before Implementation |
| `IK-CC-003` | Knowledge | knowledge | `change_control` | Impact Assessment Coverage |
| `IK-CC-004` | Knowledge | knowledge | `change_control` | Risk Assessment Before Change Release |
| `IK-CC-005` | Knowledge | knowledge | `change_control` | Implementation Control and Effective Date |
| `IK-CC-006` | Knowledge | knowledge | `change_control` | Verification After Change |
| `IK-CC-007` | Knowledge | knowledge | `change_control` | Documentation Control Across Revisions |
| `IK-CC-008` | Knowledge | knowledge | `change_control` | Audit Trail for Change Control |
| `IK-CC-009` | Knowledge | knowledge | `change_control` | Rollback Plan for Failed Change |
| `IK-CC-010` | Knowledge | knowledge | `change_control` | Human Approval Boundary for Customer-impacting Change |
| `IK-IMPR-001` | Knowledge | knowledge | `improvement` | Improvement Theme Selection for Setup Time Reduction |
| `IK-SHIP-004` | Knowledge | knowledge | `shipping` | Shipment Hold for Packing List and Lot Mismatch |
| `IR-CAPA-002` | Reasoning | reasoning | `capa` | CAPA for Torque Measurement Drift |
| `IR-FMEA-001` | Reasoning | reasoning | `fmea` | PFMEA for New Assembly Sequence |
| `IR-NCP-001` | Reasoning | reasoning | `numeric_capacity_planning` | Takt Time Feasibility Check |
| `IR-NCP-002` | Reasoning | reasoning | `numeric_capacity_planning` | Availability Adjusted Test Capacity |
| `IR-NCP-003` | Reasoning | reasoning | `numeric_capacity_planning` | Yield Adjusted Start Quantity |
| `IR-NCP-004` | Reasoning | reasoning | `numeric_capacity_planning` | Multi-process Bottleneck Capacity |
| `IR-NCP-005` | Reasoning | reasoning | `numeric_capacity_planning` | Staffing Constraint Capacity |
| `IR-NCP-006` | Reasoning | reasoning | `numeric_capacity_planning` | Required Machine Count |
| `IR-NCP-007` | Reasoning | reasoning | `numeric_capacity_planning` | Shift Run Time Capacity |
| `IR-NCP-008` | Reasoning | reasoning | `numeric_capacity_planning` | Overtime Approval Capacity |
| `IR-NCP-009` | Reasoning | reasoning | `numeric_capacity_planning` | Yield Margin and Quality Approval Boundary |
| `IR-NCP-010` | Reasoning | reasoning | `numeric_capacity_planning` | Expedite Capacity With Yield and Quality Boundary |

## 3. Categorization

### Counts by Layer

| Layer | Count |
|---|---:|
| Knowledge | 12 |
| Reasoning | 12 |
| Agent | 21 |
| Total | 45 |

### Counts by Sub-category

| Layer | Sub-category | Count |
|---|---|---:|
| Agent | `human_in_the_loop` | 10 |
| Agent | `workflow_design` | 10 |
| Agent | `tool_selection` | 1 |
| Knowledge | `change_control` | 10 |
| Knowledge | `improvement` | 1 |
| Knowledge | `shipping` | 1 |
| Reasoning | `numeric_capacity_planning` | 10 |
| Reasoning | `capa` | 1 |
| Reasoning | `fmea` | 1 |

Largest translation workloads:

1. Agent `human_in_the_loop` and `workflow_design`: 20 records
2. Knowledge `change_control`: 10 records
3. Reasoning `numeric_capacity_planning`: 10 records

## 4. Translation Difficulty Assessment

| ID | Difficulty | Rationale |
|---|---|---|
| `IK-CC-001` | Low | Administrative change-request fields; low numeric or safety complexity. |
| `IK-CC-002` | Low | Approval-before-implementation concept is direct, but approval wording must remain precise. |
| `IK-CC-003` | Medium | Impact-scope terminology must remain complete. |
| `IK-CC-004` | Medium | Risk mechanism and failure-mode language requires careful terminology. |
| `IK-CC-005` | Medium | Effective-date and production-line implementation controls must remain precise. |
| `IK-CC-006` | Medium | Verification evidence terminology must be preserved. |
| `IK-CC-007` | Medium | Documentation-control and revision terminology requires review. |
| `IK-CC-008` | Medium | Audit-trail wording must preserve traceability requirements. |
| `IK-CC-009` | Medium | Rollback planning terms need controlled translation. |
| `IK-CC-010` | High | Customer-impacting approval boundary and human approval requirements are safety-sensitive. |
| `IK-IMPR-001` | Medium | Cost-benefit and setup-time terms need numeric preservation. |
| `IK-SHIP-004` | High | Shipment hold, lot mismatch, and release decision wording are risk-sensitive. |
| `IR-CAPA-002` | High | CAPA, torque, containment, and shipment feasibility must remain equivalent. |
| `IR-FMEA-001` | High | PFMEA terminology and risk-priority concepts require domain review. |
| `IR-NCP-001` | Low | Takt calculation; low translation complexity. |
| `IR-NCP-002` | Medium | Availability-adjusted capacity terminology and numeric checks. |
| `IR-NCP-003` | Medium | Yield-adjusted start quantity terminology and rounding. |
| `IR-NCP-004` | Medium | Bottleneck terminology and multi-process reasoning. |
| `IR-NCP-005` | High | Staffing constraint and feasibility decision must remain precise. |
| `IR-NCP-006` | Medium | Required machine count and rounding requirements. |
| `IR-NCP-007` | Medium | Shift runtime capacity terminology. |
| `IR-NCP-008` | High | Overtime approval boundary and capacity feasibility. |
| `IR-NCP-009` | High | Yield margin, quality approval boundary, and escalation logic. |
| `IR-NCP-010` | High | Expedite capacity, yield, and quality boundary tradeoff. |
| `IA-HIL-004` | High | Quality hold release boundary must preserve forbidden action. |
| `IA-HIL-005` | High | Engineering change implementation approval boundary. |
| `IA-HIL-006` | High | Customer approval before shipment; customer-impacting risk. |
| `IA-HIL-007` | High | CAPA closure and effectiveness approval boundary. |
| `IA-HIL-008` | High | Maintenance work authorization and safety control. |
| `IA-HIL-009` | Medium | Overtime commitment approval and schedule risk. |
| `IA-HIL-010` | High | Supplier deviation approval boundary. |
| `IA-HIL-011` | High | Conflicting approval-state escalation. |
| `IA-HIL-012` | High | Automated document release boundary. |
| `IA-HIL-013` | High | Emergency stop-ship escalation. |
| `IA-TS-003` | Medium | Tool selection with noisy-line handover and RAG/UI terms. |
| `IA-WD-005` | High | Quality issue investigation workflow order and evidence gates. |
| `IA-WD-006` | High | Engineering change workflow and approval gates. |
| `IA-WD-007` | High | Nonconforming material disposition workflow. |
| `IA-WD-008` | High | Production recovery workflow and release constraints. |
| `IA-WD-009` | High | Supplier deviation workflow. |
| `IA-WD-010` | High | Maintenance escalation workflow. |
| `IA-WD-011` | High | Inspection plan update workflow. |
| `IA-WD-012` | High | Customer complaint response workflow. |
| `IA-WD-013` | High | Containment and release workflow. |
| `IA-WD-014` | High | Audit-ready workflow documentation. |

### Difficulty Counts

| Translation difficulty | Count |
|---|---:|
| Low | 3 |
| Medium | 16 |
| High | 26 |
| Total | 45 |

## 5. Translation Risk Assessment

| Category | Main risks |
|---|---|
| `change_control` | Meaning drift in approval, implementation boundary, verification evidence, rollback, and audit-trail terms. |
| `numeric_capacity_planning` | Numeric interpretation changes, unit conversion errors, rounding errors, feasibility decision drift, and quality-boundary ambiguity. |
| `human_in_the_loop` | Safety ambiguity, weakened forbidden-action language, unclear approver role, and missing audit-trail requirements. |
| `workflow_design` | Workflow order drift, missing gate checks, unclear handoff/escalation state, and final-state ambiguity. |
| `tool_selection` | Over-translation of RAG, UI, Teams, handover, and controlled-system terminology. |
| `improvement` | Cost-benefit interpretation, setup-time terminology, and implementation constraint drift. |
| `shipping` | Lot traceability, shipment hold, release decision, and cutoff-time interpretation errors. |
| `capa` | CAPA terminology, torque units, containment scope, and effectiveness verification drift. |
| `fmea` | PFMEA terminology, failure-mode meaning, severity/occurrence/detection concepts, and control-priority drift. |

## 6. Canonical Japanese Strategy

| Category | Recommended strategy |
|---|---|
| `change_control` | Translation plus terminology normalization; review approval, rollback, audit-trail, and customer-impacting language. |
| `numeric_capacity_planning` | Translation plus numeric/rubric review; verify all formulas, units, rounding, and feasibility decisions. |
| `human_in_the_loop` | Translation plus safety review; preserve forbidden actions, approver roles, escalation paths, and audit trail. |
| `workflow_design` | Translation plus workflow review; preserve order, gates, read-before-write behavior, final states, and evidence requirements. |
| `tool_selection` | Direct translation with terminology whitelist; keep accepted terms such as RAG, UI, Teams, and structured handover where natural. |
| `improvement` | Translation plus cost-benefit review; preserve setup-time and yen/minute calculations. |
| `shipping` | Translation plus traceability and release review; preserve hold/release language and lot-boundary meaning. |
| `capa` | Translation plus CAPA and measurement review; preserve containment, torque units, and verification of effectiveness. |
| `fmea` | Translation plus FMEA terminology review; preserve failure modes, causes, effects, and control priorities. |

## 7. Rubric Equivalence Strategy

For each translated record, reviewers should verify equivalence of:

- benchmark intent
- reference answer meaning
- `must_have` scoring criteria
- `nice_to_have` scoring criteria
- critical failures
- score caps
- numeric checks
- structured output requirements
- disallowed answers
- controlled-action boundaries
- human approval requirements
- escalation requirements
- audit-trail requirements

Recommended review method:

1. Translate the task body and rubric.
2. Back-check every scoring criterion against the English source.
3. Verify numeric values, units, tolerances, and rounding rules.
4. Verify forbidden actions and required approvals.
5. Confirm that Japanese wording is natural manufacturing-domain Japanese.
6. Mark the translated Japanese record as canonical only after reviewer approval.

## 8. Recommended Migration Order

### Priority 1: Low-risk Knowledge and Numeric Foundations

Records:

- `IK-CC-001`
- `IK-CC-002`
- `IR-NCP-001`
- medium-difficulty `change_control` records after terminology is confirmed

Justification:

These establish translation conventions for change-control terminology and numeric-capacity wording with relatively contained risk.

### Priority 2: Numeric Capacity and Change Control Completion

Records:

- remaining `IK-CC-*`
- `IR-NCP-002` through `IR-NCP-010`
- `IK-IMPR-001`
- `IK-SHIP-004`
- `IR-CAPA-002`
- `IR-FMEA-001`

Justification:

These records are central to Japanese-canonical Knowledge and Reasoning coverage. They need numeric, quality, and risk review before Agent-layer translation.

### Priority 3: Agent Approval and Workflow Records

Records:

- `IA-HIL-004` through `IA-HIL-013`
- `IA-WD-005` through `IA-WD-014`
- `IA-TS-003`

Justification:

These are the highest-risk translation items because they encode controlled actions, approval boundaries, workflow order, final states, and audit trail requirements.

## 9. Estimated Effort

Recommended batch size:

| Batch type | Records per batch | Reason |
|---|---:|---|
| Low-risk terminology batch | 3-5 | Establish shared Japanese terminology. |
| Numeric reasoning batch | 2-3 | Requires formula, unit, and tolerance review. |
| Safety/HIL batch | 2-3 | Requires approval-boundary and forbidden-action review. |
| Workflow batch | 2 | Requires ordering, gate, handoff, and final-state review. |

Recommended reviewer types:

- Japanese manufacturing-domain reviewer
- quality/change-control reviewer
- numeric capacity planning reviewer
- Agent safety / HIL reviewer
- rubric and benchmark scoring reviewer

Expected migration complexity:

| Area | Complexity |
|---|---|
| `change_control` | Medium |
| `numeric_capacity_planning` | Medium to high |
| `human_in_the_loop` | High |
| `workflow_design` | High |
| `tool_selection` | Medium |
| `improvement` | Medium |
| `shipping` | High |
| `capa` | High |
| `fmea` | High |

## 10. Success Criteria

This audit is sufficient for a future implementation phase when:

- all 45 English-only records are inventoried
- largest workload areas are identified
- translation difficulty is assigned per record
- category-level risks are documented
- Japanese-canonical migration strategy is defined by category
- rubric equivalence checks are defined
- migration priorities are clear
- no benchmark content has been modified

## 11. Recommendation

Do not start by translating all 45 records at once.

Start with a small terminology calibration batch:

```text
IK-CC-001, IK-CC-002, IR-NCP-001
```

Use that batch to establish Japanese conventions for:

- approval and change-control terminology
- numeric capacity terminology
- rubric wording
- score-cap wording
- critical-failure wording

After this calibration, proceed category by category according to the migration order above.

