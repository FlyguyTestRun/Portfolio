# Interview Map

This table maps common interview themes to the specific files and talk tracks in
this codebase. Use it to navigate the code during a technical discussion.

| Interview Theme | Primary Files | Talk Track |
|----------------|---------------|------------|
| Agentic system design | `graph/supervisor.py`, `graph/state.py` | LangGraph typed state propagates across nodes without silent field loss. Conditional edges implement routing without a meta-agent. Interrupt/resume enables HITL without a polling loop. |
| Cost governance | `graph/pre_router.py`, `rag/semantic_cache.py`, `graph/model_router.py`, `observability/cost_attribution.py` | Seven discrete layers, each with a measurable impact. Layer 7 provides empirical validation that the others are working. Combined reduction: 47 to 80 percent. |
| RAG architecture | `rag/hybrid_retriever.py`, `rag/reranker.py`, `rag/compress.py` | Hybrid retrieval (keyword + vector). Reranking before context compression. Budget-bounded context prevents token inflation. |
| Multi-modal runtime | `config.py`, `llm/clients.py`, `persistence/` | Three modes (local, hybrid, cloud) selected by environment variable. All clients degrade gracefully. Local mode runs the full graph without any cloud dependencies. |
| Compliance and safety | `governance/confidence.py`, `governance/quality_guard.py`, `governance/hitl.py` | Confidence scoring gates auto-approval. Groundedness guard prevents unanchored answers. HITL pause-and-resume for sensitive work order creation. |
| Production readiness | `Dockerfile`, `docker-compose.yml`, `api/main.py` | Non-privileged container (UID 10001). Health checks on dependencies. Lifespan context manager for startup/shutdown. Structured error handling throughout. |
| Observability | `observability/tracing.py`, `observability/cost_attribution.py` | Span context via contextvars (OTel-compatible). JSONL cost log with per-layer attribution. Cost report as an operational and CI artifact. |
| Data architecture | `persistence/pg_client.py`, `persistence/pinecone_client.py`, `persistence/redis_client.py` | pgvector for structured data and vector search locally. Pinecone for cloud-scale vector search. Redis for semantic cache. All clients wrapped with graceful connection-error handling. |
| Idempotency | `agents/maintenance_agent.py` | Idempotency key derived from sha256(run_id + asset_id + proposed_action). Retries on the same state produce the same key. Duplicate work orders are detectable at the application layer. |
| Tenant isolation | `persistence/pg_client.py`, `rag/semantic_cache.py` | All database queries filter by tenant_id. Cache keys are namespaced by tenant_id. Pinecone namespaces use `tenant_{id}` convention. |
| Testing strategy | `tests/` | Unit tests require no database or network. The pre-router, model router, confidence scorer, and quality guard are all pure functions. Integration behavior is tested via monkeypatched pg_client in test_hybrid_rag.py. |
| ADR practice | `docs/adr/` | Ten ADRs covering every major architectural decision. Each ADR records context, decision, consequences, and alternatives considered. Date-stamped and authored. |
