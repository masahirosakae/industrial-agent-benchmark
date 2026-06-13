# Benchmark Blueprint v2.0.0

This document defines the target benchmark composition for Industrial Agent Benchmark v2.0.0.

It is a planning document only. It does not modify datasets, create benchmark questions, or define private evaluation results.

## 1. Layer Structure

Industrial Agent Benchmark v2.0.0 is organized into three layers.

| Layer | Purpose | Primary judge direction |
|---|---|---|
| Knowledge | Tests industrial facts, procedures, terminology, constraints, and public reference-answer correctness. | Deterministic Judge |
| Reasoning | Tests multi-step industrial analysis, tradeoffs, root-cause reasoning, numeric planning, and evidence-supported conclusions. | Rubric Judge plus LLM Judge |
| Agent | Tests safe workflow behavior, tool use, escalation, human approval boundaries, state transitions, and auditability. | Executable Judge |

The target composition should keep the three layers balanced enough that a high overall score requires broad industrial competence, not only factual recall or text-only reasoning.

## 2. Category Structure

### Knowledge Categories

Current public categories:

- `order`
- `production_planning`
- `procurement`
- `manufacturing_preparation`
- `manufacturing_execution`
- `quality`
- `shipping`
- `improvement`
- `maintenance_engineering`

Priority candidate categories:

- `change_control`
- `compliance`
- `factory_management`

### Reasoning Categories

Current public categories:

- `5why`
- `fta`
- `fmea`
- `capa`
- `quality_improvement`
- `abnormality_analysis`
- `risk_tradeoff`
- `data_integrity`

Priority candidate category:

- `numeric_capacity_planning`

### Agent Categories

Current public categories:

- `workflow_design`
- `tool_selection`
- `human_in_the_loop`
- `hil_boundary`
- `agent_safety`
- `structured_decision`
- `tool_trajectory`
- `agent_design`
- `mcp`
- `multi_agent_coordination`

Target v2 categories should converge around the official agent capability categories:

- `workflow_design`
- `tool_selection`
- `human_in_the_loop`
- `agent_safety`
- `structured_decision`
- `tool_trajectory`

Legacy or adjacent agent categories such as `agent_design`, `mcp`, `multi_agent_coordination`, and `hil_boundary` should be reviewed for merge, rename, or explicit retention before a stable v2.0.0 release.

## 3. Target Question Counts

The target v2.0.0 benchmark should remain small enough for public iteration while large enough to be discriminative.

Recommended stable v2.0.0 target:

| Layer | Target count | Rationale |
|---|---:|---|
| Knowledge | 60 | Enough breadth for deterministic industrial knowledge checks across operations, quality, maintenance, and governance. |
| Reasoning | 60 | Supports rubric-based comparison across root cause, risk, data integrity, CAPA, and numeric planning. |
| Agent | 60 | Gives executable judge scenarios enough coverage across workflow, tool, HIL, safety, and auditability behavior. |
| Total | 180 | Balanced target that remains manageable for local evaluation and future leaderboard review. |

Recommended per-category targets:

| Layer | Category type | Target per category |
|---|---|---:|
| Knowledge | Core operational categories | 5-10 |
| Knowledge | Governance categories such as change control and compliance | 5-10 |
| Reasoning | Qualitative reasoning categories | 5-10 |
| Reasoning | Numeric reasoning categories | 10 |
| Agent | Official agent capability categories | 10 |

For v2.0.0 alpha, the current 140-question public set is acceptable as a frozen baseline while schema, loading, and evaluation workflows stabilize.

## 4. Current Coverage

Current public YAML coverage is 140 questions.

| Layer | Current count |
|---|---:|
| Knowledge | 50 |
| Reasoning | 50 |
| Agent | 40 |
| Total | 140 |

### Current Knowledge Coverage

| Category | Count |
|---|---:|
| `improvement` | 5 |
| `maintenance_engineering` | 10 |
| `manufacturing_execution` | 5 |
| `manufacturing_preparation` | 5 |
| `order` | 5 |
| `procurement` | 5 |
| `production_planning` | 5 |
| `quality` | 5 |
| `shipping` | 5 |

### Current Reasoning Coverage

| Category | Count |
|---|---:|
| `5why` | 5 |
| `abnormality_analysis` | 5 |
| `capa` | 5 |
| `data_integrity` | 10 |
| `fmea` | 5 |
| `fta` | 5 |
| `quality_improvement` | 5 |
| `risk_tradeoff` | 10 |

### Current Agent Coverage

| Category | Count |
|---|---:|
| `agent_design` | 4 |
| `agent_safety` | 5 |
| `hil_boundary` | 5 |
| `human_in_the_loop` | 3 |
| `mcp` | 3 |
| `multi_agent_coordination` | 3 |
| `structured_decision` | 5 |
| `tool_selection` | 3 |
| `tool_trajectory` | 5 |
| `workflow_design` | 4 |

## 5. Gap Analysis

### Layer Balance

The current dataset is close to balanced between Knowledge and Reasoning but underweights Agent coverage.

| Layer | Current | Stable target | Gap |
|---|---:|---:|---:|
| Knowledge | 50 | 60 | 10 |
| Reasoning | 50 | 60 | 10 |
| Agent | 40 | 60 | 20 |
| Total | 140 | 180 | 40 |

### Knowledge Gaps

The strongest gap is industrial governance knowledge:

- change control
- compliance
- customer approval boundaries
- revision and effective-date control
- audit-ready release criteria

These areas are important because they connect factual knowledge with agent safety and human approval requirements.

### Reasoning Gaps

The strongest reasoning gap is objective numeric reasoning:

- takt time
- capacity constraints
- bottleneck calculations
- OEE-sensitive planning
- staffing and equipment count reasoning
- schedule feasibility under constraints

Current reasoning coverage is strong for quality methods and risk/data integrity, but less complete for quantitative planning.

### Agent Gaps

Agent coverage should be normalized around the official capability categories.

Main gaps:

- `tool_selection`, `human_in_the_loop`, and `workflow_design` have fewer than five current items.
- `hil_boundary` overlaps with `human_in_the_loop` and should be clarified.
- `agent_design`, `mcp`, and `multi_agent_coordination` may be useful, but they are less aligned with the official executable judge categories.
- Executable state-machine scenarios are not yet represented as first-class dataset fixtures.

## 6. Priority Categories

Highest-priority v2.0.0 categories:

| Priority | Category | Layer | Reason |
|---:|---|---|---|
| 1 | `numeric_capacity_planning` | Reasoning | High discriminative value and future deterministic numeric checks. |
| 2 | `change_control` | Knowledge | Core industrial governance category with strong HIL and safety implications. |
| 3 | `human_in_the_loop` / `hil_boundary` consolidation | Agent | Critical for executable judging and safe agent behavior. |
| 4 | `tool_selection` | Agent | Needed to evaluate safe and appropriate tool use before mock execution. |
| 5 | `workflow_design` | Agent | Foundation for executable workflow validation. |
| 6 | `compliance` | Knowledge | High value but should be introduced conservatively with public-safe wording. |

Lower-priority but valuable v2.1.0 categories:

- `factory_management`
- broader `compliance`
- advanced multi-agent coordination
- richer maintenance work-order execution scenarios
- supplier quality escalation scenarios

## 7. v2.0.0 Alpha Scope

The v2.0.0 alpha scope should prioritize public usability and evaluation architecture over dataset expansion.

Recommended alpha scope:

- publish the current public YAML-derived dataset as HF-compatible JSONL
- keep the current 140 public questions as the alpha coverage baseline
- document the target 180-question stable composition
- validate dataset schema and loading
- provide simple evaluation with pre-written answer JSONL
- provide placeholder deterministic judge plumbing
- document deterministic, rubric, LLM rubric, and executable judge schemas
- avoid leaderboard implementation until result compatibility rules are stable
- avoid committing generated evaluation outputs

Optional alpha additions, only if validated public items are available:

- a small `reasoning/numeric_capacity_planning` pilot
- a small `knowledge/change_control` pilot
- normalization of overlapping HIL categories in documentation

Alpha non-goals:

- no private evaluation publication
- no leaderboard
- no benchmark question regeneration
- no provider-specific result publication
- no executable judge implementation beyond design documentation

## 8. v2.1.0 Expansion Scope

v2.1.0 should expand benchmark coverage after the v2.0.0 dataset and evaluation interfaces stabilize.

Recommended v2.1.0 expansion:

- grow toward the 180-question balanced target, or revise the target based on alpha usage
- add full `numeric_capacity_planning` coverage
- add validated `change_control` coverage
- add conservative `compliance` coverage
- decide whether `factory_management` belongs in core scope or an expansion track
- consolidate or rename overlapping agent categories
- introduce executable scenario fixtures for Agent tasks
- add structured judge metadata for Knowledge, Reasoning, and Agent results
- calibrate score compatibility across judge versions
- prepare leaderboard submission policy only after judge outputs are stable

v2.1.0 should remain public-safe: no raw private model answers, no generated local result directories, no provider secrets, and no unpublished evaluation artifacts should be committed.
