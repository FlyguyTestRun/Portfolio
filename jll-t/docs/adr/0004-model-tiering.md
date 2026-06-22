# ADR 0004: Model Tiering

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

Not every task requires frontier model capability. Classification, extraction, and
summarization tasks perform at near-identical quality on fast models (gpt-4o-mini
class) vs frontier models (gpt-4o class), at approximately 10x lower cost per token.
Sending extraction and classification tasks to frontier models is economically
indefensible when fast models handle them correctly.

The challenge is making the tier decision deterministic and auditable, not subject
to another model call.

## Decision

Layer 3 maintains a `TASK_TIER_MAP` dictionary that maps task type strings to tier
strings (`frontier` or `fast`). The mapping is code, not a prompt. Tier selection
takes microseconds and produces a deterministic, loggable result.

Frontier tasks: `reasoning`, `compliance`, `routing`.
Fast tasks: `extraction`, `classification`, `summarization`, `embedding`.

Cost constants are stored in `TIER_COST_PER_1K`: $0.015 for frontier (gpt-4o
blended estimate), $0.0015 for fast (gpt-4o-mini blended estimate).

The model tier selected for each request is recorded in state and included in the
cost log entry, enabling per-tier cost analysis.

## Consequences

Fast-tier tasks cost $0.0015 per 1,000 tokens vs $0.015 for frontier. On a mixed
workload where 60 to 70 percent of calls are extraction or classification, the
blended model cost drops by 6 to 8x for those calls.

The tier map is a single dict in one file. Adding a new task type requires one line.
The decision is deterministic and easily tested.

## Alternatives Considered

**Always use frontier for accuracy.** Rejected because extraction accuracy on
structured fields (asset IDs, status values, dates) is effectively identical on
fast and frontier models for well-specified tasks. The cost difference is 10x.

**Dynamic tier selection by a classifier model.** Rejected because meta-routing
with a model call defeats the purpose. A fast model deciding whether to use a fast
or frontier model is a cost in itself, and the decision is not more accurate than
a deterministic map for task types known at graph-design time.

**Per-prompt complexity scoring.** Rejected for Phase 1 because complexity scoring
requires either a model call or a heuristic that is no better than task-type routing.
Phase 2 could introduce RouteLLM-style complexity scoring as a Layer 3.5 between
the task-type map and the actual model call.
