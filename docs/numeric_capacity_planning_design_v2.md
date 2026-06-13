# Numeric Capacity Planning Design v2.0.0

This document defines the first content-expansion design for the `reasoning/numeric_capacity_planning` category in Industrial Agent Benchmark v2.0.0.

This is a design document only. It does not create benchmark YAML files, modify `benchmark_data/`, define private evaluation results, or introduce model-specific references.

## 1. Category Scope

Numeric Capacity Planning evaluates whether a system can reason about industrial capacity constraints using explicit calculations, units, feasibility decisions, and scenario evidence.

The category covers:

- takt time calculation from demand and available production time
- cycle time comparison against takt or required output
- equipment capacity under finite operating time
- bottleneck identification across multi-process flows
- OEE and availability effects on effective capacity
- staffing constraints and labor-limited throughput
- shift capacity, break time, planned downtime, and overtime boundaries
- yield and scrap impact on required starts or upstream workload
- schedule feasibility under demand, time, equipment, staffing, and quality constraints
- required equipment count, headcount, or shifts
- rounding constraints when partial equipment, operators, batches, or shifts are impossible

The category should focus on reasoning with public synthetic scenarios. Items should not require production-system access, proprietary process knowledge, or real customer data.

## 2. Skills Tested

Numeric Capacity Planning items should test:

- unit conversion between seconds, minutes, hours, shifts, days, units per hour, and units per shift
- capacity calculation using available time, cycle time, yield, uptime, and number of resources
- bottleneck reasoning across serial processes or constrained resources
- feasibility judgement against demand, due date, shift, staffing, and operating limits
- constraint handling when resources, approvals, overtime, quality gates, or staffing are bounded
- evidence traceability from scenario values to calculation steps and final decision
- numeric result explanation with units, assumptions, and rounding logic
- safe escalation when the plan is infeasible or depends on approval, overtime, quality risk, or missing information

Strong answers should show both the arithmetic and the operational interpretation. A correct number without a feasibility decision should not receive full credit.

## 3. Judge Mapping

Layer: Industrial Reasoning

Primary Judge: Rubric Judge

Supporting deterministic checks:

- `numeric_match`: validates expected numeric values within item-specific tolerance
- `unit_normalization`: validates equivalent units such as seconds per unit, minutes per unit, units per hour, or units per shift
- `integer_rounding_check`: validates round-up behavior for equipment count, headcount, batch count, and shift count
- `feasibility_decision_check`: validates final feasible/infeasible decision against the scenario constraints

The Rubric Judge should evaluate reasoning quality, scenario grounding, constraint use, and escalation. Deterministic checks should support the rubric but should not replace it, because many items require explanation of tradeoffs, bottlenecks, and operational risk.

## 4. Difficulty Levels

| Difficulty | Definition | Example |
|---|---|---|
| easy | Single-step calculation with one main unit conversion and no hidden constraint. | Calculate takt time from available time and daily demand. |
| medium | Capacity calculation with availability, yield, staffing, or planned downtime. | Calculate good units per shift after availability and scrap, then judge demand feasibility. |
| hard | Multi-process or multi-resource scenario requiring bottleneck identification and shift constraint handling. | Compare machining, inspection, and packing capacity under different staffing limits. |
| expert | Capacity tradeoff involving quality, overtime, escalation, or infeasible demand under multiple constraints. | Decide whether to accept an expedite request when overtime, yield loss, and quality approval boundaries affect feasibility. |

Difficulty should be determined by the number of constraints, ambiguity of the operational decision, and severity of wrong rounding or feasibility judgement.

## 5. Question Templates

### IR-NCP-001

Scenario: A line has 420 minutes of net available production time per shift after breaks and meetings. The customer requires 840 good units per shift.

Question: Calculate the required takt time in seconds per good unit and state whether a station with a 32-second cycle time can meet the demand.

Expected numeric result: Takt time = 420 minutes * 60 / 840 = 30 seconds per good unit. A 32-second cycle time is slower than takt and is not feasible without improvement or added capacity.

Expected reasoning: Convert minutes to seconds, divide by required good units, compare cycle time to takt, and conclude infeasibility.

Critical failure: Treats 32 seconds as feasible because it is close to 30 seconds, or uses minutes instead of seconds and changes the decision.

Judge notes: Deterministic checks should validate `30 seconds/unit` and `infeasible`.

### IR-NCP-002

Scenario: A test machine runs 7.5 net hours per shift. Its nominal rate is 80 units per hour, but planned availability is 85%. Daily demand is 500 tested units.

Question: Calculate the effective tested-unit capacity per shift and decide whether one machine can meet demand.

Expected numeric result: Effective capacity = 7.5 * 80 * 0.85 = 510 units per shift. One machine is feasible with a 10-unit margin.

Expected reasoning: Apply availability to nominal capacity, compare against demand, preserve units, and note the small margin.

Critical failure: Ignores availability and claims 600 units with a large margin.

Judge notes: Numeric tolerance can allow minor rounding around 510. Rubric should reward noting that the margin is small.

### IR-NCP-003

Scenario: Final assembly needs 960 good units per day. First-pass yield is 92%. Units that fail are scrapped and cannot be reworked.

Question: How many assemblies must be started to expect 960 good units, and what rounding rule applies?

Expected numeric result: Required starts = 960 / 0.92 = 1043.48, so at least 1044 assemblies must be started.

Expected reasoning: Divide required good output by yield, round up because fractional assemblies cannot be started, and explain that expected output is based on yield.

Critical failure: Rounds down to 1043 or multiplies 960 by 0.92.

Judge notes: Deterministic checks should validate both numeric value and integer round-up.

### IR-NCP-004

Scenario: A product passes through cutting, welding, and inspection. Capacities are cutting 520 units/shift, welding 460 units/shift, and inspection 500 units/shift. Demand is 480 units/shift.

Question: Identify the bottleneck and determine whether the line can meet demand.

Expected numeric result: Bottleneck capacity = welding at 460 units/shift. The line cannot meet 480 units/shift and is short by 20 units/shift.

Expected reasoning: Compare process capacities, identify the minimum capacity as the bottleneck, compare bottleneck capacity to demand, and calculate the shortfall.

Critical failure: Averages the capacities or selects the highest-capacity process as the bottleneck.

Judge notes: Deterministic checks should validate `welding`, `460`, `20 short`, and `infeasible`.

### IR-NCP-005

Scenario: A cell needs two operators to run at 120 units/hour. With one operator, the same cell is limited to 70 units/hour. Only one trained operator is available for a 6-hour net shift. Demand is 600 units today.

Question: Calculate today's feasible capacity and decide whether the schedule can be met without additional staffing.

Expected numeric result: Feasible capacity = 70 * 6 = 420 units. The schedule is short by 180 units and cannot be met without adding trained staffing, extending time within policy, or reducing demand.

Expected reasoning: Use the one-operator rate because only one trained operator is available, multiply by net shift hours, compare with demand, and identify staffing as the binding constraint.

Critical failure: Uses the two-operator rate despite only one trained operator being available.

Judge notes: Rubric should reward explicit identification of staffing as the constraint and safe escalation for additional trained labor.

### IR-NCP-006

Scenario: A machining center has a cycle time of 45 seconds per unit. It runs 2 shifts per day, each with 7 net production hours. Demand is 1,200 units per day.

Question: Calculate daily machine capacity and determine how many identical machines are required.

Expected numeric result: Capacity per machine = 2 * 7 * 3600 / 45 = 1120 units/day. Required machines = 1200 / 1120 = 1.071, so 2 machines are required.

Expected reasoning: Convert hours to seconds, calculate capacity per machine, divide demand by capacity, and round up to a whole machine.

Critical failure: Reports 1.071 machines or 1 machine as sufficient.

Judge notes: Deterministic checks should validate `1120 units/day` and `2 machines`.

### IR-NCP-007

Scenario: A packaging line can process 300 units/hour when running. It has 30 minutes of changeover, 45 minutes of planned cleaning, and an 8-hour paid shift. Demand is 2,100 units.

Question: Calculate available run time, capacity, and whether the shift plan is feasible.

Expected numeric result: Available run time = 8 - 0.5 - 0.75 = 6.75 hours. Capacity = 6.75 * 300 = 2025 units. The plan is short by 75 units and infeasible.

Expected reasoning: Subtract non-running time from paid shift, calculate productive capacity, compare to demand, and identify shortfall.

Critical failure: Uses the full 8 paid hours as running time and incorrectly claims feasibility.

Judge notes: Unit normalization should accept 405 available minutes or 6.75 hours.

### IR-NCP-008

Scenario: A supplier can ship 400 parts/day with normal staffing. Approved overtime can add 80 parts/day, but overtime requires production manager approval. Demand for the next three days is 1,380 parts.

Question: Determine whether the demand can be met under normal capacity and whether overtime escalation is needed.

Expected numeric result: Normal three-day capacity = 400 * 3 = 1200 parts. Shortfall = 180 parts. With approved overtime, capacity = 480 * 3 = 1440 parts, which can meet demand if approval is granted.

Expected reasoning: Compare normal capacity to demand, calculate shortfall, evaluate approved overtime capacity, and escalate because overtime is required and approval-bound.

Critical failure: Recommends using overtime without mentioning required approval, or claims normal capacity is sufficient.

Judge notes: Rubric should evaluate safe escalation, not only arithmetic.

### IR-NCP-009

Scenario: A line must produce 900 conforming units. The upstream process can start 1,000 units. Expected yield is 91%, but if the process is rushed above 1,000 starts, quality approval is required before release.

Question: Determine whether the current plan can meet the conforming-unit requirement and what action is needed if output is insufficient.

Expected numeric result: Expected conforming output = 1000 * 0.91 = 910 units. The plan is numerically feasible with a 10-unit expected margin. If the margin is unacceptable or more starts are needed, quality approval is required before release.

Expected reasoning: Apply yield to starts, compare conforming output to requirement, note narrow margin, and respect the quality approval boundary for any rushed or expanded production.

Critical failure: Ignores yield or recommends rushing extra starts without quality approval.

Judge notes: Rubric should reward identifying that the base plan is feasible but fragile.

### IR-NCP-010

Scenario: An expedite request requires 1,600 good units in two days. The process has two machines, each capable of 500 units/day before quality loss. Running above that rate increases scrap risk and requires quality approval. Normal yield is 96%. No additional machines are available.

Question: Assess whether the request is feasible without exceeding normal machine limits, and state the escalation decision.

Expected numeric result: Required starts for 1,600 good units = 1600 / 0.96 = 1666.67, so 1667 starts are required. Normal two-day start capacity = 2 machines * 500 units/day * 2 days = 2000 starts. The plan is feasible within normal machine limits if material and staffing are available; no above-rate quality escalation is needed for capacity, but assumptions should be confirmed.

Expected reasoning: Convert good-unit demand to required starts using yield, calculate two-day machine capacity, compare starts to capacity, avoid unnecessary overtime or above-rate running, and identify assumptions such as material and staffing.

Critical failure: Compares 1,600 good units directly to start capacity without considering yield, or recommends above-rate production when normal capacity is sufficient.

Judge notes: This is an expert item because it combines yield, multi-day equipment capacity, quality boundary, and escalation judgement.

## 6. Evaluation Rubric

Generic scoring should use the v2.0.0 Industrial Reasoning 0-5 scale.

Must-have elements:

- performs the correct calculation for the scenario
- reports the correct unit or a normalized equivalent unit
- applies all stated constraints such as availability, yield, staffing, shift time, or approval boundaries
- explains the feasibility decision rather than only reporting a number
- identifies the bottleneck when the scenario contains multiple process or resource capacities
- traces calculations to scenario evidence and states assumptions when needed
- escalates safely when the plan is infeasible, approval-bound, or dependent on missing operational information

Nice-to-have elements:

- shows intermediate calculations clearly
- states margin, shortfall, or utilization
- identifies the binding constraint explicitly
- distinguishes expected capacity from guaranteed output
- flags fragile feasibility when the numeric margin is small
- proposes practical next actions without bypassing constraints

Suggested score guidance:

| Score | Guidance |
|---:|---|
| 0 | Empty, irrelevant, or no meaningful numeric reasoning. |
| 1 | Critical failure or arithmetic/unit error that makes the decision unsafe or invalid. |
| 2 | Major calculation or constraint errors; partial scenario use but wrong final decision. |
| 3 | Plausible calculation with gaps in units, constraints, bottleneck reasoning, or explanation. |
| 4 | Correct calculation and decision with minor omissions in explanation, margin, or assumptions. |
| 5 | Correct, unit-consistent, constraint-aware, evidence-traceable answer with clear feasibility and escalation judgement. |

## 7. Critical Failures

Critical failures should normally cap the score at 1 or 2 depending on the item-specific rubric.

Examples:

- wrong unit conversion changes the operational decision
- fails to round required equipment, headcount, starts, batches, or shifts up when partial resources are impossible
- ignores the bottleneck in a multi-process scenario
- treats an infeasible plan as feasible
- ignores quality, yield, scrap, or first-pass-good constraints
- recommends unsafe overtime, unapproved overtime, or impossible capacity
- uses paid shift time as productive time when breaks, changeover, cleaning, downtime, or meetings are explicitly excluded
- uses nominal capacity when availability, OEE, or staffing constraints are provided
- invents missing resources, machines, labor, approval, or yield values not present in the scenario
- recommends release or shipment when the scenario requires escalation, approval, or confirmation

## 8. YAML Authoring Plan

The 10 candidate templates in this document should later be converted into YAML benchmark items under:

```text
benchmark_data/reasoning/numeric_capacity_planning/
```

Planned YAML IDs:

- `IR-NCP-001.yaml`
- `IR-NCP-002.yaml`
- `IR-NCP-003.yaml`
- `IR-NCP-004.yaml`
- `IR-NCP-005.yaml`
- `IR-NCP-006.yaml`
- `IR-NCP-007.yaml`
- `IR-NCP-008.yaml`
- `IR-NCP-009.yaml`
- `IR-NCP-010.yaml`

Each YAML item should include:

- stable `id`
- `category: reasoning`
- `sub_category: numeric_capacity_planning`
- public synthetic scenario and question
- reference answer with calculation steps, units, feasibility decision, and escalation guidance
- rubric with must-have elements, nice-to-have elements, critical failures, and score guidance
- deterministic check metadata when the schema supports it
- difficulty label based on the definitions in this document
- tags such as `capacity`, `takt-time`, `yield`, `bottleneck`, `oee`, `staffing`, or `feasibility`

Authoring sequence:

1. Convert the easy and medium templates first to validate schema fit.
2. Add numeric expected values and tolerances in a consistent structured form when supported.
3. Validate YAML files with `scripts/validate_dataset.py`.
4. Export JSONL with `scripts/export_hf_dataset_v2.py`.
5. Validate exported JSONL with `scripts/validate_hf_dataset_v2.py data/v2/test.jsonl`.
6. Review that no item includes private company data, real customer data, proprietary process details, or model references.

The first YAML batch should remain small and auditable. If any template proves ambiguous during authoring, revise the design document or defer that item rather than committing a weak benchmark question.

## 9. Non-goals

This category design does not include:

- production system data
- private company data
- real customer data
- proprietary process data
- live ERP, MES, QMS, CMMS, or supplier-system references
- private model answers
- model-specific evaluation outputs
- leaderboard implementation
- benchmark YAML creation in this task
- modification of `benchmark_data/`
