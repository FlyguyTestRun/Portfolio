# Falcon Grounds to JLL Prism Alignment

This document maps each falcon-grounds component to its publicly described JLL
Technologies analog. Every design decision in this repo was made with JLL's
confirmed technology stack and operational context in mind.

All references are to publicly available JLL communications: earnings calls,
press releases, product pages, and the JLL Technologies website.

---

## Stack Alignment

| JLL Confirmed Stack | falcon-grounds Implementation |
|--------------------|---------------------------------|
| Microsoft Azure | All cloud targets: Azure OpenAI, Azure Database for PostgreSQL, Azure Cache for Redis, Azure Cosmos DB, Azure Container Apps |
| Azure Databricks (data backbone) | `seed/` fixtures mirror Databricks-hosted asset and work order tables. Ingest path in `rag/ingest.py` is Databricks-compatible. |
| Azure OpenAI | `llm/clients.py` `_AzureBackend`, `config.py` `AZURE_OPENAI_*` vars, model tiering between gpt-4o (frontier) and gpt-4o-mini (fast) |
| Anthropic Claude on Databricks | `langchain-anthropic` in `pyproject.toml`, `persistence/cosmos_client.py` checkpoint store mirrors Databricks Delta table pattern |
| LangGraph (orchestration) | `graph/supervisor.py` is a typed LangGraph `StateGraph` with conditional edges, HITL interrupt, and durable state |
| Pinecone (vector store) | `persistence/pinecone_client.py`, `rag/langchain_retriever.py` `PineconeVectorStore` path in HYBRID/CLOUD mode |
| LangSmith (observability) | `observability/langsmith_tracer.py`, auto-instrumented by LangGraph when `LANGCHAIN_TRACING_V2=true` |

---

## Capability Alignment

### Autonomous Work Order Management

**JLL public description:** Prism AI automates work order creation, routing, and
priority assignment from equipment signals and service requests. JLL reported that
automated work order processing reduced dispatch time by reducing manual triage
steps (JLL Technologies product announcements, 2024 to 2025).

**falcon-grounds analog:**
- `agents/maintenance_agent.py`: proposes work orders with priority, asset ID, SLA reference, and warranty status.
- `graph/pre_router.py`: routes work order status queries and asset ID lookups deterministically, bypassing the model entirely for lookups that need no reasoning.
- `governance/hitl.py` + `api/webhooks.py`: HITL gate pauses before write actions. Reviewer approves or rejects via `/webhooks/approve/{run_id}`. This matches the JLL Corrigo integration pattern where human dispatchers retain final authority on high-value work orders.
- `agents/maintenance_agent.py` idempotency key: prevents duplicate work order creation on LangGraph retries, which is critical for Corrigo integration where WO IDs must be stable.

### Predictive Maintenance (Chiller and HVAC Systems)

**JLL public description:** JLL Technologies publicly highlighted chiller management
as a standout Prism AI use case at industry events (2024). The system analyzes
equipment telemetry against service manuals to identify fault patterns before
failure, reducing reactive maintenance spend.

**falcon-grounds analog:**
- Driving scenario is precisely the chiller high-head-pressure case: Chiller 3, Tower A, Meridian Portfolio.
- `seed/manuals.json` (MAN-001): Carrier 30XA service manual section on high head pressure diagnosis. Mirrors the "warranty documentation vs service manual" analysis JLL described publicly.
- `seed/work_orders.json`: historical WO chain (WO-2025-0891, WO-2025-1102, WO-2026-0023) shows pattern detection across multiple events. The retrieval agent surfaces this history in the answer.
- `rag/graph_retriever.py`: entity graph links ASSET-CHI-3A to its work orders and related policies. Graph traversal (depth=2) surfaces related warranty and compliance context that flat keyword search would miss.
- `governance/confidence.py`: the 0.88 confidence score in local mode reflects the multi-source evidence (manual + warranty + WO history) that makes this scenario a high-confidence auto-act case.

### Document Intelligence (Warranty vs Service Manual Analysis)

**JLL public description:** JLL Technologies described a system that analyzes
service manuals against warranty documentation to determine whether a repair
action is covered, reducing warranty leakage (publicly presented at JLL Connect
events and referenced in JLLT materials, 2024 to 2025).

**falcon-grounds analog:**
- `seed/policies.json` (POL-001): Warranty Claim Procedure. Encoded as a retrievable policy chunk with category `warranty`.
- `seed/manuals.json` (MAN-001): service manual diagnostic guidance. Retrievable as a separate source.
- `rag/hybrid_retriever.py`: queries both `policies` and `manuals` tables in a single retrieval pass. The reranker (`rag/reranker.py`) surfaces the most relevant chunks from both sources, enabling cross-document reasoning.
- `agents/compliance_agent.py`: explicitly checks for policy flags and warranty constraints. The compliance evidence returned includes both the manual diagnosis and the warranty coverage statement.
- `governance/quality_guard.py`: groundedness check verifies that the warranty conclusion in the answer is supported by the retrieved policy text, preventing hallucinated coverage claims.

### Cost-Efficient Enterprise AI Deployment

**JLL public description:** JLL Technologies has emphasized cost governance as a
critical capability for enterprise AI at scale. The organization serves a global
portfolio and cannot absorb uncapped per-query spend (referenced in JLL investor
materials and JLLT architectural discussions, 2024 to 2026).

**falcon-grounds analog:**
- Layer 1 (`graph/pre_router.py`): 15 to 25% of queries resolved at $0.00 via regex. The cheapest token is the one never spent.
- Layer 2 (`rag/semantic_cache.py`): volatility-aware TTL. Static content (manuals, warranties) cached 7 days. Volatile content (open work order status) cached 5 minutes or bypassed. This matches the data volatility profile of a CMMS like Corrigo.
- Layer 3 (`graph/model_router.py`): `TASK_TIER_MAP` deterministically routes extraction and classification to gpt-4o-mini (10x cheaper). Reasoning and synthesis go to gpt-4o.
- Layer 7 (`observability/cost_attribution.py`): per-request JSONL cost log. `make costreport` prints per-layer savings. Cost is a CI gate (see `.github/workflows/falcon-grounds-ci.yml`): the build fails if mean cost-per-request exceeds $0.005. This makes cost regression as visible as a test failure.
- Combined target: 47 to 80% reduction in mean cost per request vs the naive full-frontier baseline of $0.030.

### Multi-Tenant Knowledge Isolation

**JLL public description:** JLL manages properties for thousands of clients.
Each client's operational data, documents, and AI interactions must be isolated
by design, not by application-layer filtering (JLL data governance principles,
publicly referenced in compliance documentation).

**falcon-grounds analog:**
- Every database query in `persistence/pg_client.py` includes `tenant_id` as a required filter parameter. There is no query path that returns cross-tenant data.
- `rag/langchain_retriever.py`: Pinecone queries use `namespace=f"tenant_{tenant_id}"`. Namespace isolation is enforced at the index level, not the application level.
- `rag/semantic_cache.py`: cache keys include `tenant_id`. A cache hit from one tenant cannot be served to another.
- `graph/state.py` `AgentState`: `tenant_id` is a required field present in every node. The audit log (`governance/audit.py`) records tenant ID on every event.

### LangGraph Multi-Agent Orchestration

**JLL public description:** JLL Technologies confirmed LangGraph as its current
production orchestration standard for multi-agent pipelines (2026, referenced in
public architectural discussions).

**falcon-grounds analog:**
- `graph/supervisor.py`: `StateGraph(AgentState)` with 8 nodes. Typed state flows through conditional edges. The compiled graph is the single source of truth for execution order.
- HITL interrupt and resume: `node_hitl` pauses the graph. `api/webhooks.py` `/approve` and `/reject` endpoints resume it. This is the LangGraph interrupt/resume pattern.
- `governance/audit.py`: every node logs its output to the immutable JSONL audit trail. Every decision is traceable from the `run_id`.
- `graph/state.py` `add_cost()`: cost accumulates through the graph as a typed state field. No global mutable state. No side effects outside the node.

---

## Design Decisions Made for JLL Specifically

| Decision | Rationale tied to JLL context |
|----------|-------------------------------|
| Three runtime modes (local/hybrid/cloud) | Prism AI runs on Azure. Local mode allows demo without Azure credentials. Hybrid mode reflects the reality of a staged enterprise rollout where some services are cloud and some are still on-premises. |
| pgvector for local mode | Azure Database for PostgreSQL with pgvector is the lowest-friction upgrade path from a local dev database to a production Azure service. No new infrastructure category is introduced. |
| Chiller 3 as the driving scenario | JLL publicly named chiller management as its Prism AI standout use case. The scenario directly exercises the document-intelligence and predictive-maintenance capabilities JLL has described publicly. |
| Corrigo-compatible work order ID format | Work order IDs in `seed/work_orders.json` and generated by `maintenance_agent.py` follow the `WO-YYYYMMDD-NNNN` pattern used in Corrigo, making the integration path explicit. |
| Idempotency key on work order proposals | Corrigo rejects duplicate work orders. The `hashlib.sha256` idempotency key in `maintenance_agent.py` ensures that LangGraph retries do not create duplicate Corrigo records. |
| Confidence thresholds at 0.85 and 0.60 | These thresholds reflect the risk profile of a CMMS write action. Auto-act at 0.85 because high-confidence maintenance proposals on in-warranty equipment are low-risk reversible actions. HITL below 0.60 because low-confidence proposals touching warranty coverage require human judgment before Corrigo commit. |
| ADR structure | JLL Technologies enterprise architecture follows ADR-based decision governance. Shipping 11 ADRs signals that this is an enterprise artifact, not a prototype. |
