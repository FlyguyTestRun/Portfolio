# Cost-Control Framework

Falcon Grounds implements seven discrete cost-reduction layers applied in sequence
on every request. Each layer is a distinct code module with a measurable, auditable
impact. The layers are designed to compose: a request that hits the cache at Layer 2
never reaches Layer 3, so the savings compound rather than overlap.

## The Problem

A naive agentic architecture sends every request through a frontier model with the
full tool catalog and maximum context. At $0.015 per 1,000 tokens (gpt-4o blended
rate) and 2,000 tokens per request, the baseline cost is roughly $0.030 per request.
At 10,000 requests per month that is $300. At 100,000 requests it is $3,000. Without
attribution and governance, these costs are invisible until the invoice arrives.

## Layer 1: Deterministic Pre-Router

**Module:** `src/falcon_grounds/graph/pre_router.py`
**ADR:** ADR-0002

Regex patterns detect asset IDs, work order IDs, and named policy references in the
query text before any model call is made. Matched queries are routed directly to
`record_cost` with a zero model cost. No embeddings, no retrieval, no LLM tokens.

**Impact:** Resolves 15 to 25 percent of operational queries at zero model cost.
For a 10,000-request/month workload, this eliminates $45 to $75 of model spend.

## Layer 2: Semantic Cache

**Module:** `src/falcon_grounds/rag/semantic_cache.py`
**ADR:** ADR-0003

Redis-backed cache keyed by tenant ID and rounded query embedding. Volatility-aware
TTL: static reference data (manuals, policies) cached for 7 days. Operational data
(current alarms, open work orders) cached for 5 minutes. Work order status queries
bypass the cache entirely.

**Impact:** Cache hit rate of 40 to 60 percent on repeated queries. A cache hit
eliminates retrieval, model, and generation costs for that request entirely. The
embedding cost on miss is $0.00002 per 1,000 tokens, less than $0.001 per typical
query.

## Layer 3: Model Tiering

**Module:** `src/falcon_grounds/graph/model_router.py`
**ADR:** ADR-0004

The TASK_TIER_MAP routes reasoning and compliance tasks to frontier models and
extraction, classification, and summarization to fast models. The cost difference
is approximately 10x: $0.015/1K for frontier vs $0.0015/1K for fast.

**Impact:** On a mixed workload where 60 to 70 percent of calls are extraction or
classification (labeling assets, extracting work order fields), the blended model
cost drops to roughly $0.006 per request vs $0.015 at full frontier.

## Layer 4: Provider-Native Prompt Caching

**Module:** `src/falcon_grounds/llm/prompt_cache.py`
**ADR:** ADR-0005

System prompts for `facilities_analyst`, `compliance_checker`, and
`work_order_creator` are stable across requests. They are built once in-process and
structured to maximize provider cached-prefix utilization. The prompt is always placed
at the start of the message list and never modified between calls of the same role.

**Impact:** Up to 90 percent reduction on input token charges for the cached prompt
portion. A 300-token system prompt charged at $0.0045 on first call costs $0.00045
on subsequent calls through the provider cache.

## Layer 5: Context Compression

**Module:** `src/falcon_grounds/rag/compress.py`
**ADR:** ADR-0006

After retrieval and reranking, `compress_context()` greedily accumulates chunks until
the token budget (default 2,000 tokens) is reached. Chunks are processed in rank
order so the most relevant content always fits. Oversized single chunks are truncated
to fit the budget.

**Impact:** Reduces input tokens by 30 to 60 percent on document-heavy queries where
retrieval surfaces more content than the model needs. A query that retrieves 5,000
tokens of manual text is trimmed to 2,000 tokens before the model call.

## Layer 6: Tool-Context Discipline

**Module:** `src/falcon_grounds/tools/tool_loader.py`
**ADR:** ADR-0007

Each graph step receives only the 2 to 3 tools it can actually call, not the full
catalog. Tool definitions (descriptions and JSON schemas) typically consume 50 to 150
tokens each. A 12-tool catalog would add 600 to 1,800 tokens to every model call
regardless of which tools the step needs.

**Impact:** With a 12-tool catalog and step-specific loading of 3 tools, tool-context
discipline reduces tool-definition tokens by 75 percent per step.

## Layer 7: Cost Attribution and Governance

**Module:** `src/falcon_grounds/observability/cost_attribution.py`
**ADR:** ADR-0008

Every completed request writes a `CostEntry` to `logs/cost_log.jsonl`. The entry
records: run_id, tenant_id, query preview, cost by layer, total cost, route taken,
cache hit flag, model tier, and savings vs the $0.030 frontier baseline. The
`generate_report()` function aggregates entries for the `make costreport` report.

**Impact:** Without measurement, no optimization can be validated. Layer 7 provides
the empirical foundation for all other layers. It also enables: per-tenant cost
attribution, cost-as-CI-gate (fail if mean cost per request exceeds threshold), and
operational billing for multi-tenant deployments.

## Combined Impact

Applied together on a query mix of 20% deterministic, 45% cached, and 35% full
pipeline with mixed model tiers, the seven layers achieve 47 to 80 percent reduction
in mean cost per request compared to a naive full-frontier architecture.

The anti-drift counterpart to cost reduction is quality governance: confidence
thresholds, the groundedness guard, and the audit log prevent the system from taking
the cheapest path at the expense of answer quality.
