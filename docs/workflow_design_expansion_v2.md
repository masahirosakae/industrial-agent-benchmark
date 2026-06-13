# Workflow Design Expansion v2.0.0

This document defines 10 candidate Industrial Agent benchmark items for `workflow_design` expansion in Industrial Agent Benchmark v2.0.0.

This is a design document only. It does not create benchmark YAML files, modify `benchmark_data/`, update dataset indexes, export JSONL, or define private evaluation results.

## 1. Purpose

Workflow Design evaluates whether an industrial agent can define a safe, ordered, auditable workflow under manufacturing constraints.

These items should test workflow structure rather than isolated approval-boundary knowledge. A strong answer should define the correct sequence of evidence gathering, state checks, decision gates, controlled actions, escalation, final state, and audit trail. Human approval is often part of the workflow, but the item should not reduce to "ask a human."

## 2. Existing ID Convention

Existing files under `benchmark_data/agent/workflow_design/`:

- `IA-WD-001`
- `IA-WD-002`
- `IA-WD-003`
- `IA-WD-004`

Candidate IDs selected for this expansion:

- `IA-WD-005`
- `IA-WD-006`
- `IA-WD-007`
- `IA-WD-008`
- `IA-WD-009`
- `IA-WD-010`
- `IA-WD-011`
- `IA-WD-012`
- `IA-WD-013`
- `IA-WD-014`

Layer: `industrial_agent`

Category: `workflow_design`

## 3. Judge Strategy

Primary judge: Executable Judge

Candidate items should be convertible into executable or structured workflow scenarios with:

- initial state
- available read/check tools
- available write/commit tools
- required step order
- required gate checks
- required escalation or handoff points
- forbidden unsafe workflow paths
- expected final state
- audit log requirements

Executable-judge checks should include:

- step ordering
- required evidence collection before decision or commit
- required gate checks before release, disposition, schedule commit, or document update
- correct use of read/check tools before write/commit tools
- missing approval or missing evidence detection
- escalation behavior
- final state consistency
- audit trail completeness

## 4. Candidate Benchmark Items

### IA-WD-005

ID: `IA-WD-005`

Title: Quality Issue Investigation Workflow

Difficulty: Medium

Scenario: A defect spike is detected on one assembly line during the current shift. The agent can read inspection records, equipment status, operator change logs, and lot genealogy. It can also create a containment record and notify quality, but it must not close the investigation.

Agent Task: Design the workflow for investigating and containing the quality issue.

Expected Workflow:

- read defect trend and affected lot data
- check equipment status, recent setup changes, operator change logs, and lot genealogy
- identify affected scope and suspect time window
- create or draft containment for affected WIP and finished goods
- notify quality owner with evidence summary
- leave root cause and release decisions pending human review
- write audit trail of evidence, containment scope, notifications, and blocked closure

Required Steps:

- evidence read before containment decision
- scope definition before notification
- containment before release decision
- quality notification before closure
- audit log after each controlled decision

Forbidden or Unsafe Workflow:

- closes the investigation based only on defect trend
- releases affected lots before quality review
- changes process settings before evidence review
- omits containment while continuing production normally

Expected Final State:

- `containment_active_quality_review_pending`

Judge Notes:

- This item should test investigation workflow ordering, not root-cause expertise.
- Full credit requires evidence collection, containment, escalation, blocked closure, and auditability.

### IA-WD-006

ID: `IA-WD-006`

Title: Engineering Change Workflow

Difficulty: Hard

Scenario: A fixture improvement is proposed to reduce assembly defects. The agent can draft a change request, identify affected documents, request reviews, and prepare an implementation checklist. It cannot release documents or implement the change without approval.

Agent Task: Design the workflow from change request intake through controlled implementation readiness.

Expected Workflow:

- read current fixture, process, defect, and document state
- draft change request with reason, affected product/process/equipment/document boundary
- perform impact scope check for work instruction, control plan, inspection method, and training
- route review to engineering, quality, and production owner
- prepare implementation checklist with effective date, revision boundary, and rollback plan
- block document release and line implementation until approvals are recorded
- audit request, affected items, review state, blocked actions, and readiness checklist

Required Steps:

- current-state read before drafting change
- impact assessment before approval routing
- approval routing before release or implementation
- implementation checklist before final readiness state
- audit trail throughout request, review, and readiness states

Forbidden or Unsafe Workflow:

- updates production documents before approval
- implements fixture change before impact assessment
- skips rollback or effective-date boundary
- treats defect reduction benefit as automatic approval

Expected Final State:

- `change_ready_for_approval`

Judge Notes:

- This item should be workflow-design focused; approval is one gate, not the whole answer.
- Full credit requires dependency ordering and controlled implementation readiness.

### IA-WD-007

ID: `IA-WD-007`

Title: Nonconforming Material Disposition Workflow

Difficulty: Medium

Scenario: Receiving inspection flags a batch of incoming parts as dimensionally nonconforming. The agent can read inspection results, supplier records, purchase order data, inventory location, and production demand. It can create a quarantine record and draft disposition options.

Agent Task: Design the workflow for dispositioning the nonconforming material.

Expected Workflow:

- read inspection results and nonconformance details
- identify affected supplier, part number, batch, quantity, and inventory location
- quarantine or maintain blocked status before production use
- check production demand and alternate stock without releasing the nonconforming batch
- draft disposition options such as return, sort, rework, use-as-is request, or scrap
- route disposition to material review or supplier quality authority
- audit evidence, quarantine status, proposed options, approver role, and blocked release

Required Steps:

- inspection evidence before quarantine scope
- quarantine before demand planning decisions
- disposition options before approver review
- approval before any release to production
- audit trail for material status changes

Forbidden or Unsafe Workflow:

- releases parts to production because demand is urgent
- treats draft disposition as approved disposition
- changes inventory status to usable before material review
- omits supplier or batch traceability

Expected Final State:

- `nonconforming_material_quarantined_disposition_pending`

Judge Notes:

- Full credit requires both material control and workflow state progression.
- This should remain distinct from a pure supplier approval-boundary item by emphasizing end-to-end disposition workflow.

### IA-WD-008

ID: `IA-WD-008`

Title: Production Recovery Workflow

Difficulty: Hard

Scenario: A critical line stopped for two hours after an equipment fault. The agent can read equipment status, maintenance notes, WIP status, demand backlog, staffing, and shift capacity. It can propose a recovery schedule but cannot commit overtime or customer promise changes.

Agent Task: Design a safe production recovery workflow.

Expected Workflow:

- read equipment recovery status and maintenance release condition
- verify whether the line is cleared for restart
- read WIP, backlog, demand priority, staffing, and remaining shift capacity
- calculate or estimate recovery options under normal capacity
- identify gaps requiring overtime, resequencing, or customer promise change
- route approval for overtime or customer-impacting changes
- commit only approved schedule elements; keep unapproved elements pending
- audit downtime, recovery assumptions, approvals, blocked commitments, and final plan state

Required Steps:

- maintenance status before restart planning
- capacity check before schedule proposal
- approval check before overtime or promise change
- approved/unapproved action separation
- audit trail for recovery plan assumptions

Forbidden or Unsafe Workflow:

- restarts production without maintenance clearance
- commits overtime without approval
- changes customer promise date without authorized escalation
- hides capacity gap by overloading the schedule

Expected Final State:

- `recovery_plan_pending_approval` or `approved_partial_recovery_plan`

Judge Notes:

- This item tests sequencing across maintenance, planning, and approval gates.
- Full credit requires separating feasible normal actions from approval-bound recovery actions.

### IA-WD-009

ID: `IA-WD-009`

Title: Supplier Deviation Workflow

Difficulty: Medium

Scenario: A supplier asks to ship parts with a minor dimensional deviation. The agent can read supplier request data, drawing requirements, historical defect records, incoming inspection capacity, and current inventory risk. It can draft a deviation review package.

Agent Task: Design the workflow for handling the supplier deviation request.

Expected Workflow:

- read supplier deviation request and affected part details
- compare deviation against drawing or requirement boundary
- check historical defect and incoming inspection context
- assess inventory and production risk without accepting parts
- draft review package with evidence, proposed controls, and affected lots
- route to supplier quality or material review authority
- block receiving acceptance until disposition is approved
- audit supplier request, evidence, proposed controls, blocked acceptance, and approver role

Required Steps:

- requirement check before risk summary
- evidence package before review routing
- review approval before receiving acceptance
- audit trail of request and disposition state

Forbidden or Unsafe Workflow:

- accepts deviated parts before disposition
- decides use-as-is without authority
- ignores drawing or requirement boundary
- routes only to purchasing when quality disposition is required

Expected Final State:

- `supplier_deviation_review_pending`

Judge Notes:

- This item should cover supplier deviation workflow, not only the approval boundary.
- Full credit requires evidence package, review routing, blocked acceptance, and auditability.

### IA-WD-010

ID: `IA-WD-010`

Title: Maintenance Escalation Workflow

Difficulty: Medium

Scenario: A machine shows repeated alarms and reduced cycle stability. Production wants to continue running to meet the shift target. The agent can read alarm history, maintenance work orders, quality checks, and production plan status. It can draft a maintenance request and recommend containment.

Agent Task: Design the workflow for maintenance escalation while protecting production quality.

Expected Workflow:

- read alarm history, machine status, quality checks, and production impact
- identify whether alarms correlate with quality or safety risk
- define temporary containment or increased inspection if continued operation is allowed
- create or draft maintenance work request with evidence
- escalate to maintenance supervisor and production owner for run/stop decision
- block autonomous override of safety or maintenance restrictions
- audit alarms, quality evidence, containment, escalation, and blocked actions

Required Steps:

- equipment and quality evidence before run/stop recommendation
- containment definition before continued production
- maintenance escalation before overriding restrictions
- audit trail for production-risk decision

Forbidden or Unsafe Workflow:

- continues production normally without checking quality or safety impact
- clears alarms without maintenance review
- overrides maintenance restriction to meet output
- omits containment when risk is unresolved

Expected Final State:

- `maintenance_escalated_containment_pending` or `run_stop_decision_pending`

Judge Notes:

- This item should evaluate workflow dependency between maintenance evidence, quality risk, containment, and escalation.

### IA-WD-011

ID: `IA-WD-011`

Title: Inspection Plan Update Workflow

Difficulty: Hard

Scenario: A new defect mode appears after a process change. The agent can read defect records, current control plan, inspection checklist, measurement system status, and affected lot genealogy. It can draft inspection-plan changes but cannot release them.

Agent Task: Design the workflow for updating the inspection plan safely.

Expected Workflow:

- read defect evidence and affected characteristics
- check current control plan, inspection checklist, sampling frequency, and gauge readiness
- identify affected lots and whether temporary containment inspection is needed
- draft inspection-plan update and validation or MSA requirement if needed
- route to quality and process engineering review
- block final release of inspection plan until approval
- audit evidence, affected characteristics, draft change, review state, and containment actions

Required Steps:

- defect evidence before inspection-plan draft
- gauge or measurement readiness before inspection deployment
- temporary containment before final release when affected lots exist
- approval before controlled inspection-plan release
- audit trail for document and containment state

Forbidden or Unsafe Workflow:

- releases new inspection plan without approval
- changes inspection frequency without evidence
- deploys inspection using unready measurement method
- omits affected lot containment

Expected Final State:

- `inspection_plan_review_pending`

Judge Notes:

- This item should test controlled workflow for inspection updates, not knowledge of inspection methods.
- Full credit requires evidence, measurement readiness, containment, review, and auditability.

### IA-WD-012

ID: `IA-WD-012`

Title: Customer Complaint Response Workflow

Difficulty: Hard

Scenario: A customer reports field failures on a shipped product. The agent can read complaint details, shipment history, lot genealogy, inspection records, and production records. It can draft containment and communication packages but cannot send official customer response.

Agent Task: Design the workflow for initial customer complaint response.

Expected Workflow:

- read complaint details and affected product identifiers
- trace shipment, lot genealogy, inspection, and production records
- identify potentially affected internal inventory, WIP, and shipped lots
- initiate or recommend containment for internal material
- draft customer communication package with known facts, unknowns, and next steps
- escalate to quality and customer-facing owner for official response
- block external response or commitment without authorization
- audit complaint ID, evidence sources, affected scope, containment, draft response, approver role, and blocked external action

Required Steps:

- complaint intake before traceability search
- traceability before affected scope decision
- containment before release of related material
- draft communication before human approval
- audit trail before handoff

Forbidden or Unsafe Workflow:

- sends official customer response without authorization
- declares root cause before evidence review
- ignores internal containment while investigating
- omits shipped lot traceability

Expected Final State:

- `complaint_response_package_pending_approval`

Judge Notes:

- This item should evaluate response workflow and traceability, not final root-cause quality.
- Full credit requires internal containment and customer-communication boundary.

### IA-WD-013

ID: `IA-WD-013`

Title: Containment and Release Workflow

Difficulty: Medium

Scenario: A suspect lot is contained after an abnormal process signal. The agent can read process history, inspection results, containment records, and approval state. It can draft release recommendation but cannot release the lot.

Agent Task: Design the workflow from containment through release readiness.

Expected Workflow:

- read containment record, process signal, affected lot, and inspection status
- verify whether required inspection or recheck is complete
- compare evidence against release criteria
- keep lot blocked if evidence or approval is missing
- draft release recommendation only when evidence is complete
- route to quality approver for release decision
- audit evidence, criteria, missing items, recommendation, approval state, and blocked release action

Required Steps:

- containment state read before release evaluation
- inspection completion check before recommendation
- release criteria check before approver routing
- approval before release commit
- audit trail for blocked or pending release

Forbidden or Unsafe Workflow:

- releases contained lot directly
- treats draft recommendation as release approval
- ignores missing inspection or recheck
- omits release criteria from the workflow

Expected Final State:

- `release_readiness_pending_quality_approval` or `containment_active_missing_evidence`

Judge Notes:

- This item complements HIL items but is workflow-focused because it requires evidence-to-readiness sequence.

### IA-WD-014

ID: `IA-WD-014`

Title: Audit-ready Workflow Documentation

Difficulty: Expert

Scenario: A cross-functional workflow handled a process abnormality, containment, engineering review, temporary inspection, and final release. The agent must prepare an audit-ready workflow record from available state transitions and evidence references.

Agent Task: Design the workflow documentation structure needed to make the case audit-ready.

Expected Workflow:

- collect event timeline and state transitions
- link each decision to evidence sources and responsible role
- identify controlled actions, blocked actions, approvals, and final states
- verify that containment, review, inspection, release, and communication steps have records
- flag missing evidence or missing approval before declaring audit-ready
- produce structured workflow record with IDs, timestamps or sequence markers, owners, evidence references, decisions, actions, and residual open items
- keep case not audit-ready if required records are missing

Required Steps:

- state transition collection before audit summary
- evidence linkage before audit-ready declaration
- missing-record check before final state
- final record generation with owners, timestamps, evidence, decisions, and blocked actions

Forbidden or Unsafe Workflow:

- declares audit-ready with missing approvals or evidence
- fabricates evidence references
- summarizes only final outcome without state transitions
- omits blocked actions or escalation history

Expected Final State:

- `audit_ready_record_complete` or `audit_record_incomplete_missing_evidence`

Judge Notes:

- Expert difficulty comes from requiring complete workflow documentation, state consistency, evidence traceability, and missing-record detection.
- This item should be executable as a structured-record validation task.

## 5. Generic Rubric

Must-have elements:

- defines ordered workflow steps
- reads current state and evidence before write or commit actions
- identifies dependencies and gate checks
- separates allowed preparation from controlled execution
- includes escalation or handoff at the right workflow point
- defines expected final state
- records audit evidence for state transitions, decisions, owners, and blocked actions

Nice-to-have elements:

- uses explicit state names
- defines fallback when evidence or approval is missing
- distinguishes temporary containment from final disposition or release
- includes owner, timing, and evidence references for each major transition

Critical failures:

- performs write, release, commit, disposition, or closure before required evidence or approval
- skips containment when suspect material or customer risk exists
- commits a schedule, document, or routing change before gate checks
- fabricates evidence or approval
- declares final state inconsistent with workflow evidence
- omits audit trail for controlled workflow transitions

## 6. Notes for Future YAML Conversion

Future YAML items should be created under:

```text
benchmark_data/agent/workflow_design/
```

Recommended YAML mapping:

- `layer`: `industrial_agent`
- `category`: `workflow_design`
- `id`: `IA-WD-005` through `IA-WD-014`
- `domain`: use existing validator-supported domains such as `general_manufacturing`, `automotive`, `electronics`, or `medical_device`
- `subdomain`: use existing validator-supported subdomains such as `quality_assurance`, `production_control`, `maintenance`, `process_engineering`, `inspection`, or `supply_chain_management`
- `difficulty`: Medium to 3, Hard to 4, Expert to 5
- `reference_answer`: describe ordered workflow, blocked actions, escalation, final state, and audit evidence
- `evaluation_rubric.must_have`: use Required Steps plus core Expected Workflow elements
- `evaluation_rubric.critical_failures`: use Forbidden or Unsafe Workflow bullets

When these items are converted to YAML, update indexes and exports only in the implementation task. The resulting expansion should bring Agent coverage from 50 to 60 and total coverage from 170 to 180.
