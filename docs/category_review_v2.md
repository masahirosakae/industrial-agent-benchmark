# Benchmark Category Review for v2.0.0

This review covers four candidate categories for Industrial Agent Benchmark v2.0.0:

- `knowledge/change_control`
- `knowledge/compliance`
- `knowledge/factory_management`
- `reasoning/numeric_capacity_planning`

## Current State

The candidate directories currently contain no question YAML files. Each directory has only a `.gitkeep` placeholder.

| Candidate category | Current YAML question count | Planned scope found in docs |
|---|---:|---:|
| `knowledge/change_control` | 0 | 10 planned titles |
| `knowledge/compliance` | 0 | 10 planned titles |
| `knowledge/factory_management` | 0 | 10 planned titles |
| `reasoning/numeric_capacity_planning` | 0 | 10 planned titles |

Because no candidate question YAMLs exist yet, this review evaluates category value, scope, and duplication risk based on the category names and existing planning notes rather than completed benchmark items.

## Existing Category Context

Current adjacent categories already represented in YAML:

| Layer | Category | Count |
|---|---|---:|
| Knowledge | `order` | 5 |
| Knowledge | `production_planning` | 5 |
| Knowledge | `procurement` | 5 |
| Knowledge | `manufacturing_preparation` | 5 |
| Knowledge | `manufacturing_execution` | 5 |
| Knowledge | `quality` | 5 |
| Knowledge | `shipping` | 5 |
| Knowledge | `improvement` | 5 |
| Knowledge | `maintenance_engineering` | 10 |
| Reasoning | `risk_tradeoff` | 10 |
| Reasoning | `data_integrity` | 10 |
| Reasoning | `fta`, `5why`, `fmea`, `capa`, `quality_improvement`, `abnormality_analysis` | 5 each |

## Category Summaries

### `knowledge/change_control`

Scope: Engineering change control, 4M changes, ECN/PCN handling, PPAP implications, customer approval gates, traceability during changeover, rollback planning, and emergency change handling.

Strengths:

- High industrial relevance: change approval and release timing are frequent failure points.
- Strong connection to agent safety and human approval boundaries.
- Tests whether a model respects customer approval, PPAP, regulatory notification, and traceability constraints.
- Can create discriminative tasks with disallowed premature-release answers.

Weaknesses:

- Easy to blur into generic quality, manufacturing preparation, or data integrity unless scenarios are tightly scoped.
- Requires careful rubric design to avoid rewarding broad change-management boilerplate.
- May need domain-specific references, which increases validation burden.

Overlap risks:

- `quality`: approval, containment, PPAP, and nonconformance handling.
- `manufacturing_preparation`: process validation and launch readiness.
- `data_integrity`: traceability and version boundary control.
- `agent/hil_boundary`: customer or QA approval before execution.

Benchmark value: High. This is a core manufacturing governance category that complements existing operational categories.

Recommendation: Include in v2.0.0 if at least a small, validated public set can be created. Otherwise defer complete coverage to v2.1.0. Do not merge; keep as a distinct category because change approval semantics are not equivalent to general quality or preparation.

### `knowledge/compliance`

Scope: Regulatory and standards compliance, audit records, traceability requirements, RoHS/REACH, ISO/IATF/FDA-style constraints, export-control checks, supplier code compliance, recall/reporting timing, and required escalation.

Strengths:

- Strong benchmark value for industrial deployment because compliance mistakes can be high impact.
- Good at testing abstention, escalation, source grounding, and refusal to treat uncertain compliance status as cleared.
- Complements data integrity and HIL categories through audit trail and approval requirements.
- Can expose generic-answer failures when a model ignores specific regulatory thresholds or document requirements.

Weaknesses:

- High risk of legal/regulatory overclaiming if prompts are not carefully framed as benchmark scenarios.
- Requires public-safe references and rubrics that avoid implying operational legal advice.
- Can become jurisdiction-specific and brittle.

Overlap risks:

- `quality`: audit, traceability, recall, and certification topics.
- `data_integrity`: evidence, records, and source completeness.
- `risk_tradeoff`: stop-ship versus release decisions under uncertainty.
- `agent_safety` and `hil_boundary`: escalation when compliance status is uncertain.

Benchmark value: High, but only with careful wording and clear non-advice framing.

Recommendation: Include selectively in v2.0.0 only if the first items are conservative, public-safe, and framed around process judgment rather than legal interpretation. Defer broader coverage to v2.1.0. Do not merge; compliance should remain distinct from quality because it tests regulatory/evidence discipline.

### `knowledge/factory_management`

Scope: Factory economics, investment decisions, NPV/IRR/payback, insource versus outsource decisions, break-even analysis, KPI trees, staffing/shift decisions, currency sensitivity, leasing versus purchase, and site consolidation.

Strengths:

- Expands the benchmark beyond shop-floor quality into plant-management decision making.
- Good source of numeric, financial, and strategic tradeoff questions.
- Tests practical industrial reasoning that many agent systems will need for planning and operations support.
- Can improve coverage of management-level decisions and business constraints.

Weaknesses:

- Some planned topics are closer to business/finance than industrial-agent execution.
- Risk of overlap with `risk_tradeoff` and `numeric_capacity_planning`.
- May dilute benchmark identity if too much weight shifts from manufacturing operations to finance.

Overlap risks:

- `risk_tradeoff`: investment versus operational risk, night-shift decisions, outsourcing tradeoffs.
- `production_planning`: capacity and line utilization.
- `maintenance_engineering`: equipment investment and lifecycle cost.
- `numeric_capacity_planning`: resource/load calculations.

Benchmark value: Medium to high. Valuable for industrial management coverage, but less urgent than change control and numeric capacity planning.

Recommendation: Defer to v2.1.0, or include only a small v2.0.0 pilot subset if category balance allows. Keep distinct if included, but enforce a boundary: factory management should focus on plant-level economic decisions, while numeric capacity planning handles operational capacity math.

### `reasoning/numeric_capacity_planning`

Scope: Capacity calculations, takt/cycle-time reasoning, OEE decomposition, bottleneck ROI, safety stock, makespan sequencing, staffing constraints, EPEI, seasonal leveling, expected uptime, and required equipment counts.

Strengths:

- Very high discriminative value because answers can be checked numerically.
- Directly addresses a major industrial-agent capability: quantitative planning under constraints.
- Complements the v2 schema and simple evaluator roadmap because numeric checks can later become deterministic scoring components.
- Reduces reliance on subjective judge interpretation.

Weaknesses:

- Requires careful tolerances and unambiguous units.
- Some items may be too close to `production_planning` unless they emphasize reasoning and calculation rather than domain knowledge.
- Harder questions may need structured outputs for reliable automated validation.

Overlap risks:

- `production_planning`: capacity and schedule planning.
- `risk_tradeoff`: bottleneck investments and inventory/overwork tradeoffs.
- `factory_management`: investment and staffing economics.
- `maintenance_engineering`: equipment count and uptime calculations.

Benchmark value: Very high. This is the strongest candidate for v2.0.0 because it supports objective scoring and improves benchmark discriminative power.

Recommendation: Include in v2.0.0. Keep as a distinct reasoning category, not merged into production planning. The category should focus on numeric reasoning, constraints, and verifiable calculations.

## Duplication Risks

| Candidate | Highest duplication risk | Mitigation |
|---|---|---|
| Change Control | `quality`, `manufacturing_preparation`, `data_integrity`, `hil_boundary` | Require explicit change-trigger, approval, revision boundary, or rollback semantics. |
| Compliance | `quality`, `data_integrity`, `risk_tradeoff`, `hil_boundary` | Require compliance-specific evidence, audit, threshold, or escalation criteria. |
| Factory Management | `risk_tradeoff`, `production_planning`, `numeric_capacity_planning` | Restrict to plant-level economic and management decisions. |
| Numeric Capacity Planning | `production_planning`, `risk_tradeoff`, `factory_management` | Require explicit calculations, units, tolerances, and capacity constraints. |

## Recommendations

| Category | Recommendation | Rationale |
|---|---|---|
| `reasoning/numeric_capacity_planning` | Include in v2.0.0 | Highest objective-scoring value and strongest fit for HLE-style benchmark workflows. |
| `knowledge/change_control` | Include in v2.0.0 if validated items are available; otherwise defer to v2.1.0 | High industrial value and distinct approval semantics, but needs careful public rubrics. |
| `knowledge/compliance` | Defer broad coverage to v2.1.0; include only conservative pilot items in v2.0.0 if needed | High value but higher wording and regulatory-risk burden. |
| `knowledge/factory_management` | Defer to v2.1.0 | Useful, but lower urgency and higher overlap with risk, production planning, and finance-like tasks. |

## Final Recommendation

For v2.0.0, prioritize `reasoning/numeric_capacity_planning` and a small, well-scoped `knowledge/change_control` subset if authoring capacity allows. Defer broad `knowledge/compliance` and `knowledge/factory_management` coverage to v2.1.0.

Do not merge `numeric_capacity_planning` into `production_planning`; doing so would lose the distinction between knowledge of planning concepts and quantitative reasoning under constraints.

Do not merge `change_control` into `quality`; change approval, customer notification, PCN/ECN/PPAP boundaries, and rollback decisions form a distinct industrial-agent capability.
