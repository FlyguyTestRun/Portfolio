# Architecture

## Overview

Falcon Grounds is a reference implementation of a governed agentic system for
facilities management. The core problem it solves: agentic AI systems fail in two
ways. They drift in cost as usage grows, and they drift in quality as model responses
lose grounding in source data. This architecture addresses both failure modes
explicitly through a seven-layer cost-control framework and a mandatory groundedness
check on every answer.

## System Diagram

```
                     FALCON GROUNDS: GOVERNED AGENT ARCHITECTURE

  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                          REQUEST FLOW                                       │
  │                                                                             │
  │   User Query                                                                │
  │       │                                                                     │
  │       ▼                                                                     │
  │  ┌─────────┐   LAYER 1: Deterministic Pre-Router                           │
  │  │ Pre-    │   Regex patterns resolve hard signals at zero model cost.      │
  │  │ Router  │   Asset IDs, work order numbers, named policies.               │
  │  └────┬────┘                                                                │
  │       │ (no match)                                                          │
  │       ▼                                                                     │
  │  ┌─────────┐   LAYER 2: Semantic Cache                                     │
  │  │ Cache   │   Redis-backed, keyed by tenant and rounded embedding.         │
  │  │ Check   │   Static data: 7-day TTL. Volatile data: 5-min TTL.           │
  │  └────┬────┘   Work order status: bypass.                                  │
  │       │ (miss)                                                              │
  │       ▼                                                                     │
  │  ┌─────────┐   LAYER 3: Model Router                                       │
  │  │ Model   │   Right-sizes tier per task. Reasoning uses frontier.          │
  │  │ Router  │   Extraction and classification use fast (10x cheaper).        │
  │  └────┬────┘                                                                │
  │       │                                                                     │
  │       ▼                                                                     │
  │  ┌─────────────────────────────────────────┐                               │
  │  │           LANGGRAPH SUPERVISOR           │                               │
  │  │                                         │                               │
  │  │  ┌──────────┐  ┌──────────┐  ┌───────┐ │   LAYER 4: Prompt Caching    │
  │  │  │Retrieval │  │Compliance│  │Maint. │ │   Stable system prompts       │
  │  │  │ Agent    │→ │ Agent    │→ │ Agent │ │   cached at provider level.   │
  │  │  └──────────┘  └──────────┘  └───────┘ │                               │
  │  │                                         │   LAYER 5: Context Compress.  │
  │  │              LAYER 6:                   │   Top-k truncation before     │
  │  │              Tool Context Discipline    │   each model call.            │
  │  └─────────────────────────────────────────┘                               │
  │           │                                                                 │
  │           ▼                                                                 │
  │  ┌─────────────┐   Quality Guard: groundedness check.                      │
  │  │ Quality     │   Ungrounded answers retry retrieval (max 3 iterations).  │
  │  │ Guard       │                                                            │
  │  └──────┬──────┘                                                           │
  │          │                                                                  │
  │          ▼                                                                  │
  │  ┌─────────────┐   HITL Gate: interrupt and webhook.                       │
  │  │ HITL Gate   │   Low-confidence or flagged actions pause for approval.   │
  │  └──────┬──────┘   Reviewer approves or rejects via webhook.               │
  │          │                                                                  │
  │          ▼                                                                  │
  │  ┌─────────────┐   LAYER 7: Cost Attribution                               │
  │  │ Cost Record │   Per-layer cost logged to JSONL.                         │
  │  └─────────────┘   'make costreport' aggregates and reports.               │
  │                                                                             │
  │  DATA LAYER                                                                 │
  │  PostgreSQL (local) / Azure Database for PostgreSQL (cloud)                 │
  │  Redis (local) / Azure Cache for Redis (cloud)                              │
  │  Pinecone (hybrid/cloud only)                                               │
  │  Azure Cosmos DB (hybrid/cloud, checkpoint storage)                         │
  └─────────────────────────────────────────────────────────────────────────────┘
```

## Components

### Gateway (FastAPI)
`src/falcon_grounds/api/main.py`. Receives POST /query requests. Calls `run_query()`
from the supervisor graph. Exposes GET /cost-report for operational visibility. The
lifespan context manager initializes the PostgreSQL schema on startup.

### Deterministic Pre-Router (Layer 1)
`src/falcon_grounds/graph/pre_router.py`. Runs before any model call. Matches
asset IDs, work order IDs, and named policy references using compiled regex patterns.
Resolves roughly 15 to 25 percent of operational queries at zero cost.

### Semantic Cache (Layer 2)
`src/falcon_grounds/rag/semantic_cache.py`. Redis-backed. Cache key is sha256 of
tenant ID and rounded query embedding (3 decimal places). TTL is selected per
query volatility. Bypass tags prevent stale work order status from being cached.

### Model Router (Layer 3)
`src/falcon_grounds/graph/model_router.py`. Deterministic code, not a prompt.
Maps task type to model tier. Reasoning and compliance use frontier. Extraction,
classification, and summarization use fast (10x lower cost per token).

### LangGraph Supervisor
`src/falcon_grounds/graph/supervisor.py`. Compiled StateGraph with typed AgentState.
Nodes are deterministic Python functions. Conditional edges implement routing logic.
The graph is stateless per request and safe to invoke concurrently.

### Retrieval Agent
`src/falcon_grounds/agents/retrieval_agent.py`. Queries PostgreSQL for relevant
assets, work orders, policies, and service manuals. Applies hybrid retriever,
reranker, and context compression. Returns ranked, budget-bounded chunks.

### Compliance Agent
`src/falcon_grounds/agents/compliance_agent.py`. Scores confidence based on
retrieval coverage and answer quality. Checks for warranty and policy constraints.
Sets `requires_hitl` flag when confidence is below threshold or policy flags are raised.

### Maintenance Agent
`src/falcon_grounds/agents/maintenance_agent.py`. Proposes a work order action.
Generates a stable idempotency key from run_id, asset_id, and proposed action.
Composes the final answer combining the proposed action with compliance evidence.

### Quality Guard
`src/falcon_grounds/governance/quality_guard.py`. Checks that key terms in the
answer appear in the retrieved context. Ungrounded answers re-enter the retrieval
node (up to 3 iterations). This prevents the model from generating answers that
are not supported by the knowledge base.

### HITL Gate
`src/falcon_grounds/governance/hitl.py`. Pauses execution for human review when
confidence is low or compliance flags are raised. In local mode, uses a console
prompt. In cloud mode, posts to a webhook and returns pending. The /webhooks/approve
and /webhooks/reject endpoints record the decision.

### Cost Attribution (Layer 7)
`src/falcon_grounds/observability/cost_attribution.py`. Writes a CostEntry to
`logs/cost_log.jsonl` after every request. Tracks cost by layer, route type,
model tier, and savings vs a full-frontier baseline.

## Two Failure Modes

**Cost drift.** Model costs grow silently as usage increases. Without per-request
cost attribution (Layer 7) and pre-routing optimizations (Layers 1 to 6), the
cost per query defaults to the frontier rate on every call. The seven-layer framework
reduces mean cost by 47 to 80 percent depending on query mix.

**Hallucination drift.** Model answers drift away from source data as prompts
evolve or retrieval quality degrades. The quality guard (groundedness check) flags
answers where fewer than 40 percent of key terms appear in the retrieved context.
Flagged answers retry retrieval before being surfaced to the user.

## Cross-Cutting Concerns

**Audit trail.** Every graph node logs an event to `logs/audit.jsonl` and, in
cloud mode, to the PostgreSQL `audit_log` table.

**Idempotency.** The maintenance agent generates a stable idempotency key from
run_id, asset_id, and proposed action. Duplicate work order submissions on retry
are detectable and suppressable.

**Tenant isolation.** All database queries filter by tenant_id. All Pinecone
operations use tenant-namespaced namespaces. Cost log entries include tenant_id
for per-tenant billing.

## Data Layer

Local: PostgreSQL (pgvector extension) for structured data and Redis for caching.
Hybrid: Azure Database for PostgreSQL + Azure Cache for Redis + Pinecone for
vector search.
Cloud: All above plus Azure Cosmos DB for durable graph checkpoint storage.
