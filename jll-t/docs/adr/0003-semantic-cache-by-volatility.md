# ADR 0003: Semantic Cache with Volatility TTL

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

Facilities management data has two distinct volatility classes. Reference data
(equipment specifications, service manuals, policies, warranty terms) changes rarely.
Operational data (work order status, active alarms, current equipment readings)
changes frequently. A single TTL for both is wrong: too short wastes cache hits on
reference data, too long serves stale work order status to users.

Additionally, natural language queries for the same underlying information often
differ in phrasing. "What does the Carrier manual say about head pressure?" and
"Carrier 30XA high head pressure causes" are semantically identical but lexically
different. Exact-match string caching misses these.

## Decision

Layer 2 implements semantic caching with volatility-aware TTL selection. Cache keys
are sha256 of tenant_id concatenated with the query embedding rounded to 3 decimal
places. The 3-decimal rounding buckets near-duplicate embeddings together without
requiring exact float equality.

TTL selection logic:
- If any bypass tag (e.g., `work_order_status`, `open_wo`) appears in the query:
  return 0 (bypass entirely).
- If volatile signals (`status`, `open`, `pending`, `current`, `today`, `live`,
  `now`) appear in the query: return `CACHE_TTL_VOLATILE` (5 minutes).
- Otherwise: return `CACHE_TTL_STATIC` (7 days).

## Consequences

Cache hit rates of 40 to 60 percent on repeated queries. A cache hit eliminates
retrieval, model, and generation cost entirely for that request. Embedding cost on
miss is $0.00002 per 1,000 tokens, less than $0.001 per typical query.

Work order status is always fresh. Reference data (manuals, policies) is cached for
7 days, reflecting the actual update frequency of that content.

Connection errors to Redis are handled gracefully. The cache returns a miss result,
and the request proceeds through the full pipeline. Redis unavailability degrades
performance but does not break correctness.

## Alternatives Considered

**Exact-match cache on query string.** Rejected because natural language phrasing
variation produces many cache misses for semantically identical queries. Users phrase
the same question differently on different days.

**Single TTL for all queries.** Rejected because a TTL appropriate for work order
status (minutes) would eliminate all value from caching reference data, and a TTL
appropriate for reference data (days) would serve stale operational data.

**No caching.** Rejected because caching is the highest-leverage single optimization
for a query-heavy workload. It is also the most operationally transparent: cache hits
and misses are logged and reported.
