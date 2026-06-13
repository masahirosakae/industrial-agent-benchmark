# Change Control Design v2.0.0

This document defines 10 candidate benchmark items for the `knowledge/change_control` category in Industrial Agent Benchmark v2.0.0.

This is a design document only. It does not create benchmark YAML files, modify `benchmark_data/`, update dataset indexes, export JSONL, or define private evaluation results.

## 1. Purpose

Change Control evaluates whether a system understands core manufacturing change-control concepts, required records, approval boundaries, implementation discipline, and verification expectations.

This category belongs to the Industrial Knowledge layer. Items should test factual and procedural knowledge that can be judged deterministically through required points, keyword coverage, and explicit critical omissions.

The category supports the v2.0.0 expansion target by adding a governance-focused Knowledge category that connects naturally to future Agent-layer workflows, especially approval gates, human-in-the-loop boundaries, and auditability.

## 2. Scope

In scope:

- change request intake and required information
- impact assessment across product, process, quality, supplier, tooling, documentation, and customer boundaries
- risk assessment before implementation
- approval workflow and release gates
- implementation control and effective-date management
- verification after change
- documentation control and revision alignment
- audit trail and record retention concepts
- rollback planning and containment if a change fails
- human approval boundary before executing or releasing a controlled change

Out of scope:

- private company-specific change-control procedures
- proprietary production data or customer data
- legal advice or regulatory interpretation
- narrow certification wording that depends on a specific clause text
- broad consulting strategy that cannot be judged with deterministic expected points
- live PLM, ERP, MES, QMS, or customer-portal operation

## 3. Knowledge Areas

The 10 candidate items collectively cover:

| Knowledge area | Coverage |
|---|---|
| Change request | Required fields, trigger, reason, affected item, proposed change, owner |
| Impact assessment | Product, process, tooling, documentation, supplier, customer, quality impact |
| Risk assessment | Failure mode, severity, affected lots, validation need, containment risk |
| Approval workflow | Required approvers and no-implementation-before-approval boundary |
| Implementation control | Effective date, revision, work instruction, training, and release control |
| Verification after change | First article, trial run, inspection, capability, or acceptance evidence |
| Documentation control | Revision control, obsolete document prevention, aligned records |
| Audit trail | Who requested, reviewed, approved, implemented, verified, and when |
| Rollback planning | Criteria, containment, reversion path, disposition of affected material |
| Human approval boundary | Agent or system must not execute, release, or ship before required human approval |

## 4. Difficulty Distribution

Balanced distribution:

| Difficulty | Count | Intended item IDs |
|---|---:|---|
| Easy | 2 | `IK-CC-001`, `IK-CC-002` |
| Medium | 4 | `IK-CC-003`, `IK-CC-004`, `IK-CC-005`, `IK-CC-006` |
| Hard | 3 | `IK-CC-007`, `IK-CC-008`, `IK-CC-009` |
| Expert | 1 | `IK-CC-010` |

Difficulty is based on the number of required knowledge points, the number of affected functions, and whether the item requires distinguishing approval, implementation, verification, and release boundaries.

## 5. Judge Strategy

Layer: Industrial Knowledge

Primary judge: Deterministic Judge

Candidate items should be answerable through clear expected points and keywords. The judge should not need to evaluate subjective strategy quality.

Suggested deterministic checks:

- required keyword or concept presence
- required checklist element coverage
- forbidden action detection
- approval-boundary detection
- documentation and audit-trail element detection
- explicit yes/no or allow/block decision for controlled actions

Expected scoring direction:

- Full credit requires all core required points and no unsafe approval-boundary violation.
- Partial credit can be awarded for correct but incomplete checklist coverage.
- Critical failures should cap the score when an answer permits implementation, release, shipment, or document use before required approval or verification.

## 6. Candidate Benchmark Items

### IK-CC-001

ID: `IK-CC-001`

Title: Required Change Request Fields

Difficulty: Easy

Question: A production engineer wants to submit a change request for a fixture modification that may also change a process parameter and the inspection method on one production line. Name the minimum manufacturing information that should be included before review begins.

Expected Points:

- affected product, part number, production line, process step, fixture, equipment, or inspection method
- description of the proposed fixture, process parameter, or inspection method change
- reason or trigger for the change, such as defect reduction, equipment issue, productivity improvement, or customer requirement
- requester or owner
- target timing or proposed effective date
- initial affected documents or records, such as drawing, control plan, work instruction, setup sheet, inspection checklist, or fixture record

Keywords:

- change request
- affected item
- product boundary
- process boundary
- equipment boundary
- inspection method
- proposed change
- reason
- owner
- effective date
- document revision

Judge Notes:

- Deterministic judge should require at least affected manufacturing boundary, proposed change, reason, owner, and timing or effective date.
- Full credit should mention at least one production boundary such as product/part, line/process step, fixture/equipment, inspection method, or controlled document.
- Do not require ISO-specific terminology.
- Answers that only say "get approval" without describing request content should receive low credit.

### IK-CC-002

ID: `IK-CC-002`

Title: Change Approval Before Implementation

Difficulty: Easy

Question: A supervisor says a tooling change is simple and asks the team to implement it before the change request is approved. What is the correct change-control response?

Expected Points:

- do not implement the controlled change before required approval
- keep the current approved process or tooling in use
- route the change request through the defined review and approval workflow
- document any urgent need through the approved escalation path

Keywords:

- approval
- do not implement
- controlled change
- escalation
- current approved process
- change workflow

Judge Notes:

- The expected decision is to block implementation until required approval is obtained.
- A critical failure is allowing implementation because the change appears simple.
- This item prepares future Agent-layer human approval boundary scenarios.

### IK-CC-003

ID: `IK-CC-003`

Title: Impact Assessment Coverage

Difficulty: Medium

Question: A proposed process parameter change may affect product dimensions and inspection frequency. For the impact assessment, list the scope areas that must be checked to identify what is affected by the change.

Expected Points:

- affected products, part numbers, variants, or customer programs
- affected process steps, production lines, equipment, fixtures, tooling, or software settings
- affected inspection plans, control plans, gauges, test methods, or sampling frequency
- affected drawings, work instructions, setup sheets, forms, or other controlled documents
- affected lots, WIP, inventory, shipment status, or effective-date boundary
- affected suppliers, customers, downstream processes, packaging, or service parts when applicable

Keywords:

- impact assessment
- affected product
- affected process
- tooling
- equipment
- inspection plan
- control plan
- work instruction
- affected lots
- supplier impact
- customer impact
- downstream process

Judge Notes:

- Deterministic judge should reward checklist coverage.
- Full credit should require scope coverage across product, process/equipment/tooling, inspection/control plan, documentation, and affected material or lot boundary.
- This item should focus on identifying what is affected, not evaluating how severe each risk is.
- Do not require a long consulting-style risk matrix.

### IK-CC-004

ID: `IK-CC-004`

Title: Risk Assessment Before Change Release

Difficulty: Medium

Question: Before releasing a material substitution, what risk mechanisms or failure modes should be checked to avoid unintended manufacturing or quality issues?

Expected Points:

- what could go wrong because of the material change, including fit, form, function, strength, contamination, durability, appearance, or processability
- severity or quality impact if the failure mode occurs
- compatibility with existing process conditions, equipment, tooling, gauges, and inspection methods
- need for containment of affected inventory, WIP, or early production output
- need for trial run, validation, inspection evidence, or capability confirmation
- approval requirement before use in production or shipment

Keywords:

- risk assessment
- specification
- compatibility
- failure mode
- severity
- quality impact
- containment
- validation
- inspection
- affected lots
- approval

Judge Notes:

- The item is knowledge-focused: expected answer is a bounded checklist.
- Full credit should include failure mode, quality or severity impact, process/equipment compatibility, validation or inspection need, containment need, and approval before production use.
- This item should focus on what could go wrong and what evidence or containment is needed, not merely listing affected scope areas.
- Critical failure: says the substitute material can be used immediately without approval or verification.

### IK-CC-005

ID: `IK-CC-005`

Title: Implementation Control and Effective Date

Difficulty: Medium

Question: A process change is approved, but some work instructions and line labels still show the old revision. What controls are needed before implementation on the production line?

Expected Points:

- confirm approved effective date or implementation point
- update and release controlled documents before use
- remove or obsolete old instructions at the point of use
- communicate or train affected operators
- confirm line labels, setup sheets, or related records match the new revision
- keep evidence of implementation completion

Keywords:

- effective date
- released document
- obsolete document
- point of use
- training
- revision
- implementation record

Judge Notes:

- Full credit should distinguish approval from controlled implementation.
- Critical failure: allows production to run with mixed old and new instructions.
- Judge can check for effective date, document update, obsolete removal, training/communication, and implementation evidence.

### IK-CC-006

ID: `IK-CC-006`

Title: Verification After Change

Difficulty: Medium

Question: A fixture change has been implemented on an assembly line. What verification evidence should be collected before the change is considered complete?

Expected Points:

- inspection or measurement results for affected characteristics
- first article, trial run, or initial production check
- confirmation that acceptance criteria are met
- review of any defects, abnormalities, or process instability
- record of who verified the change and when
- linkage to the approved change request

Keywords:

- verification
- inspection result
- first article
- trial run
- acceptance criteria
- abnormality
- verified by
- change request

Judge Notes:

- Deterministic judge should expect evidence, criteria, and traceability to the approved change.
- Answers that only say "check quality" without evidence or acceptance criteria should receive partial credit.
- Do not require a specific statistical method unless stated in the question.

### IK-CC-007

ID: `IK-CC-007`

Title: Documentation Control Across Revisions

Difficulty: Hard

Question: An approved engineering change updates a drawing, control plan, work instruction, and inspection checklist. What documentation-control actions are required to prevent mixed-revision production?

Expected Points:

- release the new controlled revisions together or by a defined effective sequence
- remove, block, or obsolete old revisions at points of use
- ensure drawing, control plan, work instruction, and checklist revisions are aligned
- communicate the effective date or lot/serial boundary
- retain revision history and approval records
- verify that production uses only the current released documents

Keywords:

- controlled revision
- obsolete
- point of use
- aligned documents
- effective date
- lot boundary
- revision history
- approval record

Judge Notes:

- Full credit requires both document alignment and old-revision prevention.
- Critical failure: treats updating one document as sufficient while other controlled documents remain old.
- Deterministic checks should look for alignment, obsolete removal, effective boundary, and audit record.

### IK-CC-008

ID: `IK-CC-008`

Title: Audit Trail for Change Control

Difficulty: Hard

Question: A quality auditor asks for the audit trail of a completed process change. What records should be available to show the change was controlled?

Expected Points:

- original change request and reason
- impact and risk assessment records
- review and approval records with approver identity and date
- implementation record with effective date or lot boundary
- updated document revision history
- verification or validation evidence after implementation
- disposition of affected WIP, inventory, or lots if applicable

Keywords:

- audit trail
- change request
- impact assessment
- risk assessment
- approval record
- effective date
- revision history
- verification evidence
- affected lots

Judge Notes:

- This item should be judged as a record checklist.
- Full credit should require request, assessment, approval, implementation, document revision, and verification evidence.
- Do not require private system names such as a specific PLM or QMS product.

### IK-CC-009

ID: `IK-CC-009`

Title: Rollback Plan for Failed Change

Difficulty: Hard

Question: A newly implemented process change causes defects during the first production run. What elements should a rollback plan include?

Expected Points:

- criteria for stopping or reversing the change
- containment of affected product, WIP, or lots
- approved method to return to the previous validated process or revision
- notification or approval from required functions before rollback when applicable
- re-verification after rollback
- documentation of defect evidence, rollback action, and final disposition

Keywords:

- rollback
- stop criteria
- containment
- previous revision
- approved process
- re-verification
- disposition
- documentation

Judge Notes:

- Full credit requires containment, return path, re-verification, and records.
- Critical failure: continues production with defects or rolls back without controlling affected material.
- Keep the item knowledge-based; do not ask for detailed root-cause strategy.

### IK-CC-010

ID: `IK-CC-010`

Title: Human Approval Boundary for Customer-impacting Change

Difficulty: Expert

Question: A change to a manufacturing process may affect a customer-approved or customer-impacting characteristic. An automated system has enough information to update the work instruction, change the released revision, and mark the process ready for production. What must the system not do by itself, and what approvals, checks, and evidence are required before production release?

Expected Points:

- the automated system must not release, implement, or mark the change production-ready by itself
- required human approval boundary must be enforced before document release, production implementation, or shipment
- customer-approved or customer-impacting characteristic must be identified explicitly
- responsible human functions such as quality, engineering, manufacturing, and the customer-facing approval owner must review or approve as applicable
- customer notification or customer approval boundary must be checked when the change can affect a customer-approved characteristic
- impact assessment must identify affected product, process, document, inspection, lot, and customer boundaries
- risk assessment must identify potential failure modes, severity or quality impact, containment need, and validation need
- verification or validation evidence must be required before production release
- audit trail must record who approved, what was released, when it was released, and the basis for the release decision

Keywords:

- human approval
- do not release
- do not implement
- production-ready
- customer-impacting
- customer-approved characteristic
- quality approval
- engineering approval
- customer approval
- customer notification
- impact assessment
- risk assessment
- verification
- validation
- audit trail

Judge Notes:

- This is still a Knowledge item, but it is compatible with future Agent-layer human-in-the-loop scenarios.
- Critical failure: says the automated system may release, implement, or mark production-ready solely because it has enough information.
- Deterministic judge should require "must not release/implement without human approval" plus customer-impacting characteristic, customer notification or approval boundary, impact assessment, risk assessment, verification or validation evidence, and audit trail.
- The item should not ask the model to design an executable workflow; it should test knowledge of the approval and evidence requirements.

## 7. Notes for Future YAML Conversion

Future YAML items should be created under:

```text
benchmark_data/knowledge/change_control/
```

Planned YAML IDs:

- `IK-CC-001.yaml`
- `IK-CC-002.yaml`
- `IK-CC-003.yaml`
- `IK-CC-004.yaml`
- `IK-CC-005.yaml`
- `IK-CC-006.yaml`
- `IK-CC-007.yaml`
- `IK-CC-008.yaml`
- `IK-CC-009.yaml`
- `IK-CC-010.yaml`

Recommended YAML mapping:

- `layer`: `industrial_knowledge`
- `category`: `change_control`
- `domain`: use public-safe manufacturing domains such as `general_manufacturing`, `automotive`, `electronics`, or `medical_device`
- `subdomain`: choose from existing validator-supported subdomains such as `quality_assurance`, `process_engineering`, `production_control`, `assembly`, or `inspection`
- `difficulty`: map Easy to 1-2, Medium to 3, Hard to 4, Expert to 5
- `reference_answer`: use the Expected Points and a concise explanation
- `evaluation_rubric.must_have`: use required Expected Points
- `evaluation_rubric.nice_to_have`: include useful but nonessential traceability or implementation details
- `evaluation_rubric.critical_failures`: include approval-boundary violations and unsafe release/implementation statements

Before YAML conversion, update validator category metadata only if needed for `change_control`. Do not update dataset indexes or `data/v2/test.jsonl` until the YAML files are intentionally added and validated.

The first YAML batch should preserve deterministic judgeability. If an item starts to require subjective consulting advice, it should be rewritten as a checklist, yes/no approval-boundary decision, or short factual answer.
