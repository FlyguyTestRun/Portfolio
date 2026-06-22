# falcon-grounds

Reference architecture for governed agentic facilities-management AI on Azure.

---

## The Cost Problem

Agentic AI systems fail in two ways. They drift in cost as usage grows, and they
drift in quality as model responses lose grounding in source data.

**Cost drift.** A naive implementation sends every query through a frontier model
with the full tool catalog and maximum context. At $0.015 per 1,000 tokens (gpt-4o
blended) and 2,000 tokens per request, the baseline is $0.030 per request. At 100,000
requests per month, that is $3,000. Without per-request attribution, this is invisible
until the invoice arrives.

**Hallucination drift.** Model answers drift away from source data as prompts evolve
or retrieval quality degrades. Without a mandatory groundedness check, degradation
goes undetected. Users receive confident, unfounded answers.

Falcon Grounds addresses both with a seven-layer cost-control framework and a
quality guard on every answer.

---

## Architecture

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
  │  │ Cost Record │   Per-request JSONL cost log.                              │
  │  └─────────────┘   'make costreport' aggregates and reports.               │
  │                    Cost gate in CI fails build on regression.               │
  │                                                                             │
  │  DATA LAYER                                                                 │
  │  PostgreSQL (local) / Azure Database for PostgreSQL (cloud)                 │
  │  Redis (local) / Azure Cache for Redis (cloud)                              │
  │  Pinecone (hybrid/cloud only)                                               │
  │  Azure Cosmos DB (hybrid/cloud, checkpoint storage)                         │
  └─────────────────────────────────────────────────────────────────────────────┘
```

---

## Seven-Layer Cost Framework

| Layer | Description | Module | Measurable Impact |
|-------|-------------|--------|-------------------|
| 1: Pre-Router | Regex resolves hard signals at zero model cost | `graph/pre_router.py` | 15 to 25% of queries at $0.00 |
| 2: Semantic Cache | Volatility-aware TTL, tenant-namespaced | `rag/semantic_cache.py` | 40 to 60% cache hit rate |
| 3: Model Tiering | Frontier for reasoning, fast for extraction | `graph/model_router.py` | 10x cost reduction on fast-tier tasks |
| 4: Prompt Caching | Stable prompts cached at provider | `llm/prompt_cache.py` | Up to 90% reduction on prompt token charges |
| 5: Context Compression | Top-k truncation before model call | `rag/compress.py` | 30 to 60% input token reduction |
| 6: Tool-Context Discipline | Step-specific tool loading only | `tools/tool_loader.py` | 70 to 80% reduction in tool-definition tokens |
| 7: Cost Attribution | Per-request JSONL cost log, CI gate | `observability/cost_attribution.py` | Empirical validation, build fails on regression |

Combined: 47 to 80% reduction in mean cost per request vs naive full-frontier baseline.

---

## What This Demonstrates

| Capability | Location |
|-----------|----------|
| LangGraph typed StateGraph with HITL | `graph/supervisor.py`, `graph/state.py` |
| Seven-layer cost governance | All layer files + `observability/cost_attribution.py` |
| Cost regression as a CI gate | `.github/workflows/falcon-grounds-ci.yml`, ADR 0012 |
| Volatility-aware semantic cache | `rag/semantic_cache.py` |
| Hybrid retrieval (keyword + vector) | `rag/hybrid_retriever.py`, `rag/reranker.py` |
| Graph RAG via networkx | `rag/graph_retriever.py` |
| Groundedness guard with retry loop | `governance/quality_guard.py` |
| Confidence scoring | `governance/confidence.py` |
| Three-mode runtime (local/hybrid/cloud) | `config.py`, `llm/clients.py`, `persistence/` |
| LangSmith auto-instrumentation | `observability/langsmith_tracer.py` |
| Non-privileged Docker container | `Dockerfile` |
| FastAPI with lifespan and health endpoint | `api/main.py` |
| ADR documentation (12 decisions) | `docs/adr/` |
| Eval harness with cost gate | `eval/run_eval.py`, `eval/langsmith_eval.py` |
| Prism/Falcon alignment | `docs/falcon-prism-alignment.md` |

---

## Confirmed Stack

| Component | Technology |
|-----------|-----------|
| LLM (frontier) | Azure OpenAI gpt-4o |
| LLM (fast) | Azure OpenAI gpt-4o-mini |
| Agent framework | LangGraph StateGraph |
| Vector store (local) | pgvector (PostgreSQL extension) |
| Vector store (cloud) | Pinecone |
| Semantic cache | Redis |
| Checkpoint store | Azure Cosmos DB |
| API framework | FastAPI + uvicorn |
| Validation | Pydantic v2 |
| Language | Python 3.12 |
| Container | Docker (python:3.12-slim, UID 10001) |
| Orchestration | Docker Compose (local) / Azure Container Apps (cloud) |
| Observability | LangSmith (auto-instrumented via LangGraph) |

---

## Quickstart

```bash
# Clone and enter the project.
git clone https://github.com/FlyguyTestRun/JLL-T.git
cd JLL-T

# Copy environment template.
cp .env.example .env

# Start services and seed data (postgres + redis + api).
make up

# Run the Chiller 3 scenario end-to-end.
make demo

# View cost breakdown.
make costreport
```

No Azure credentials are required for `make demo`. All model calls use the local
stub client, which returns deterministic responses and exercises the same code paths
as the real pipeline.

---

## Sample Cost Report Output

```
falcon-grounds cost report

Summary
Metric                            Value
Total requests                    5
Total cost (USD)                  $0.01500
Total savings vs baseline (USD)   $0.13500
Cache hits                        2
Pre-route hits (zero model cost)  1

Cost by Layer
Layer          Total Cost (USD)   Description
retrieval      $0.00500           PostgreSQL keyword/vector search
maintenance    $0.00400           Work order proposal generation
compliance     $0.00000           LLM confidence and policy assessment
supervisor     $0.00150           Model tier selection (fast tier)

Requests by Model Tier
Tier         Count
fast         3
frontier     1
none         1
```

---

## ADR Index

| ADR | Title | One-Line Rationale |
|-----|-------|--------------------|
| 0001 | LangGraph Supervisor Pattern | Typed state, conditional routing, and interrupt-resume HITL in a compiled graph. |
| 0002 | Deterministic Pre-Routing | Regex resolves 15 to 25% of queries at zero cost. Code beats model for hard signals. |
| 0003 | Semantic Cache with Volatility TTL | Different TTLs for static vs volatile data. Near-duplicate embedding bucketing. |
| 0004 | Model Tiering | 10x cost difference between frontier and fast. Deterministic map, not a classifier. |
| 0005 | Provider-Native Prompt Caching | Stable prompts cached at provider. Up to 90% reduction on prompt token charges. |
| 0006 | Context Compression | Greedy top-k budget reduces input tokens 30 to 60% on document-heavy queries. |
| 0007 | Tool-Context Discipline | Step-specific tool loading prevents catalog-size token inflation per call. |
| 0008 | Cost Attribution Governance | Without measurement, no optimization can be validated. Cost as CI gate. |
| 0009 | HITL via Graph Interrupt and Webhook | Pause-and-resume for sensitive actions. Local console or cloud webhook. |
| 0010 | Three-Mode Runtime Parity | Local, hybrid, cloud. Same graph, same code paths. Mode selection by env var. |
| 0011 | LangChain Ecosystem Integration | LangChain retriever abstractions and LangSmith observability in one platform. |
| 0012 | Cost Regression as a CI Gate | Build fails if mean cost per request exceeds threshold. Regressions caught before merge. |

---

## Make Targets

| Target | Description |
|--------|-------------|
| `make up` | Build and start all services. Seeds data after startup. |
| `make down` | Stop all services. |
| `make demo` | Run the Chiller 3 scenario in local mode. |
| `make costreport` | Print cost breakdown from the JSONL log. |
| `make seed` | Load fixture data into PostgreSQL. |
| `make test` | Run the unit test suite. |
| `make eval` | Run the eval harness against chiller_queries.json. |
| `make langsmith-push-eval` | Run eval and push results to LangSmith dataset. |
| `make reset` | Drop and recreate schema. Delete logs. |
| `make logs` | Follow the API container logs. |

---

## Demo Scenario

The core scenario: "Chiller 3 in Tower A is reporting intermittent high head
pressure. What is the history, what is the likely cause, is there a warranty or
compliance constraint, and what work order should we open?"

The graph retrieves work order history (WO-2025-0891, WO-2025-1102, WO-2026-0023),
cross-references the Carrier 30XA service manual for diagnosis guidance, checks
POL-001 (Warranty Claim Procedure) and POL-002 (High Priority Equipment Response),
confirms active warranty coverage through 2029-03-15, and proposes a preventive
maintenance work order.

---

## License

MIT License. Copyright 2026 Bryan Shaw.
