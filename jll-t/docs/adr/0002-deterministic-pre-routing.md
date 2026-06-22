# ADR 0002: Deterministic Pre-Routing

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

Not every query needs a model. Asset identifier lookups, work order status checks
by ID, and named policy retrievals can be resolved with regex at zero cost. Sending
these through the full agent pipeline wastes tokens and adds latency that is
perceptible to the user.

In facilities management workloads, a substantial fraction of queries are
operational: "What is the status of work order WO-2026-0023?" or "Look up
ASSET-CHI-3A." These have unambiguous, hard-coded patterns. They do not require
reasoning.

## Decision

Layer 1 of the cost framework intercepts queries with recognizable hard signals
before the graph starts. The pre-router (`src/falcon_grounds/graph/pre_router.py`)
runs compiled regex patterns against the query text and the request context. Matched
queries are flagged `deterministic` and route directly to `record_cost`, skipping all
agent nodes.

The pre-router returns a `PreRouteResult` dataclass. The `resolved` field controls
routing. The `action` field is a constrained enum value. The `cost_usd` field is
always 0.0 for deterministic routes.

## Consequences

Typical hit rate of 15 to 25 percent of operational queries eliminates model cost
for those requests entirely. The pre-router is easily extended with new patterns
by adding a compiled regex and a corresponding action string. False positives (over-
matching) are guarded by requiring the action returned to be a specific value.

The pre-router executes in microseconds. Latency for deterministic queries drops
from the model round-trip time (hundreds of milliseconds) to sub-millisecond.

## Alternatives Considered

**Let the supervisor model decide routing.** Rejected because this costs tokens on
every request and introduces non-determinism in routing that is hard to test.
Routing decisions that can be made by a regex should not be made by a model.

**Keyword matching without regex.** Rejected because keyword matching on tokens like
"asset" would produce false positives on queries that mention assets without
providing an ID. Compiled regex patterns with specific structure (colon, space,
uppercase alphanumeric) are precise without being brittle.
