# ADR 0008: Cost Attribution and Governance

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

Cost optimization without measurement is unverifiable. Teams claim cost reductions
but cannot demonstrate them at the request level. Without per-tenant, per-feature
attribution, it is impossible to validate that optimizations are working, identify
which query types are most expensive, set CI cost gates, or produce per-tenant
billing data for multi-tenant deployments.

The standard alternative, relying on provider billing dashboards, aggregates all
costs into a single number with no request-level or feature-level breakdown.

## Decision

Layer 7 records a `CostEntry` for every completed request. Each entry is written
as a JSON line to `logs/cost_log.jsonl`. The entry includes:
- `run_id`, `tenant_id`, `query_preview` (first 80 characters)
- `timestamp` (ISO 8601 UTC)
- `layers`: dict of layer name to cost in USD
- `total_cost_usd`, `route`, `cache_hit`, `model_tier`
- `savings_usd`: FRONTIER_BASELINE ($0.030) minus total cost

The `generate_report()` function aggregates all entries into a `CostReport`.
`make costreport` prints the report using Rich tables.

## Consequences

`make costreport` shows validated, empirical cost savings with no manual calculation.
Cost can be used as a CI gate: the eval harness checks that every query costs less
than `MAX_COST_PER_REQUEST_USD`. Per-tenant billing becomes possible by filtering
the JSONL log. Identifying expensive query types requires a single `jq` command.

The JSONL format is append-only and requires no schema migration. It is readable by
BigQuery, Azure Log Analytics, and standard Unix tools.

## Alternatives Considered

**Rely on provider billing dashboards.** Rejected because dashboards aggregate by
API key, not by request. There is no way to attribute cost to individual features,
tenants, or optimization layers.

**Sampling a percentage of requests.** Rejected for Phase 1 because request volume
is low and full logging is inexpensive. Sampling reduces accuracy of the cost report
without meaningful operational benefit at current scale.

**Real-time cost alerting only, no log.** Rejected because alerting without a log
prevents retrospective analysis. The historical log is required for trend analysis
and ADR validation.
