# ADR 0012: Cost Regression as a CI Gate

**Status:** Accepted  
**Date:** 2026-06-22

---

## Context

The seven-layer cost-control framework is only as durable as its measurement. Cost
reduction claims made in architecture review lose credibility if there is no
mechanism to detect when those reductions regress. Without a gate, a change that
reverts model tiering, expands context, or widens the tool catalog silently raises
cost per request. The regression is invisible until the billing invoice arrives.

The problem is not exotic. Common regressions in production agentic systems:

- A new task type added to TASK_TIER_MAP defaults to frontier when fast would suffice.
- A retrieval retry loop introduced for quality reasons runs unconditionally rather
  than only when retrieval returns results.
- Context compression thresholds raised to improve answer quality, doubling input tokens.
- A new tool registered in STEP_TOOL_MAP for all steps rather than the one step that
  needs it.

Each of these has happened in this codebase. The CI gate caught two of them before
merge (supervisor routing classified as frontier, quality guard retrying empty retrieval).

---

## Decision

Cost per request is a CI gate. The build fails if mean cost across the eval suite
exceeds a configured threshold. This is implemented in
`.github/workflows/falcon-grounds-ci.yml` as a dedicated `cost-gate` job that runs
after `test` passes.

Mechanism:

1. The `cost-gate` job runs `eval/run_eval.py` against the full chiller query dataset.
2. Each query writes a cost entry to `logs/cost_log.jsonl` via `record_cost_entry()`.
3. A Python inline script loads the log, computes mean cost per request, and exits
   with code 1 if mean cost exceeds `COST_GATE_THRESHOLD_USD` (default: $0.005).
4. The job always prints the full cost report as a build artifact, even on failure.

The threshold is set at `$0.005` per request. At the Layer 3 model tiering settings
(supervisor on fast, frontier for reasoning/compliance), a full pipeline pass in local
mode costs approximately `$0.003` per request. The threshold gives a 65% headroom
before the gate trips, enough to absorb legitimate cost increases while catching
regressions that meaningfully change the cost profile.

---

## Consequences

**Positive:**

- Cost regressions are caught at the PR stage, not at the billing stage.
- Every engineer who changes model routing, retrieval, or tool loading sees the cost
  impact before merge.
- The gate doubles as living documentation: the cost report printed on every run shows
  exactly which layers are expensive and by how much.
- The threshold is a configuration variable (`COST_GATE_THRESHOLD_USD` env var) so it
  can be adjusted as the pipeline evolves without touching workflow YAML.

**Negative / tradeoffs:**

- The gate runs in local mode with the stub LLM client, so costs are estimated rather
  than measured against real Azure OpenAI pricing. The estimates are calibrated to
  gpt-4o-mini and gpt-4o blended rates but are not live.
- A legitimately expensive new capability (e.g., adding a reranking LLM call) will
  fail the gate and require the threshold to be updated. This is intentional friction:
  every threshold increase must be a conscious decision, not an accident.
- The gate does not currently distinguish between cost increases caused by quality
  improvements (acceptable) and cost increases caused by inefficiency (not acceptable).
  That distinction requires a combined cost-and-quality eval, deferred to Phase 4.

---

## Alternatives Considered

**Alert-only (no build failure):** A Slack or email alert when cost rises more than
10% would surface the regression without blocking the build. Rejected because soft
alerts are routinely suppressed under delivery pressure. Only a hard failure creates
durable incentive to fix the underlying cause.

**Post-deploy cost monitoring:** Track cost in production via the `cost_log.jsonl`
mechanism and alert when a rolling average rises. Useful as a second line of defense
but not a replacement for a pre-merge gate. By the time production cost rises, the
causing commit has already shipped.

**LangSmith cost tracking:** LangSmith traces include token counts and can be used
to compute per-run cost. This is implemented for hybrid and cloud modes via
`observability/langsmith_tracer.py`. It does not substitute for the CI gate because
LangSmith requires a live API key and is not available in the local CI environment.
