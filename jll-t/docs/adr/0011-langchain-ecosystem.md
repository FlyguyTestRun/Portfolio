# ADR 0011: LangChain Ecosystem Integration

**Status:** Accepted
**Date:** 2026-06-21

## Context

falcon-grounds uses LangGraph for graph orchestration. The broader LangChain
ecosystem provides three complementary capabilities not yet present: a standard
retriever abstraction (BaseRetriever) that lets the vector backend be swapped
without touching agent code, Graph RAG via networkx or Neo4j for multi-hop entity
traversal, and LangSmith for distributed tracing and eval dataset management.

Cost observability has been Layer 7 from the start. Adding LangSmith closes the
observability gap at the LLM-call level: every LangGraph node becomes a traced
span automatically when LANGCHAIN_TRACING_V2 is set. The eval harness (eval/run_eval.py)
gains a companion (eval/langsmith_eval.py) that pushes scored results to LangSmith
datasets, making routing accuracy, groundedness, and cost-per-request regressions
visible in the LangSmith dashboard.

## Decision

Adopt the following LangChain products alongside the existing LangGraph orchestration:

**LangSmith** for distributed tracing and eval dataset management. LangGraph
auto-instruments every node when LANGCHAIN_TRACING_V2=true and LANGCHAIN_API_KEY
is set. No changes required in supervisor.py beyond calling configure_langsmith()
at API startup. New module: observability/langsmith_tracer.py.

**langchain-postgres and langchain-pinecone** via FalconRetriever(BaseRetriever)
in rag/langchain_retriever.py. The retriever dispatches by RUNTIME_MODE: keyword
search over PostgreSQL in LOCAL, PGVector in HYBRID, Pinecone in CLOUD. Agent
code sees only List[Document] regardless of backend. The existing hybrid_retriever.py
remains active in LOCAL mode for zero-dependency demo runs.

**Graph RAG via networkx** in rag/graph_retriever.py. FacilitiesGraphRetriever
builds a DiGraph from seed data (assets to work orders, assets to manuals, assets
to policies). After standard retrieval, enrich() traverses edges to depth 2 and
appends related entity summaries as additional context chunks. Controlled by
GRAPH_RETRIEVAL_ENABLED=false (off by default). In CLOUD mode with
GRAPH_BACKEND=neo4j, delegates to Neo4jGraph from langchain-community.

**langchain-anthropic** adds Claude via the standard ChatModel interface. Model
tiering (ADR 0004) controls when Claude is selected versus Azure OpenAI.

## Alternatives Considered

**Raw Pinecone SDK only.** Already in use. Does not provide traced retrieval spans
or a swappable interface. No standardized document schema means each consumer must
parse Pinecone response objects directly.

**OpenTelemetry only.** Provides traces but no eval datasets, no per-run scoring,
and no LangSmith UI for comparing runs over time.

**LlamaIndex.** Different graph abstraction and orchestration model. LangGraph is
already committed as the supervisor layer (ADR 0001). Adding a second orchestration
framework increases cognitive and dependency overhead.

## Consequences

Six new production dependencies: langsmith, langchain-community, langchain-postgres,
langchain-pinecone, langchain-anthropic, networkx. All pinned to major versions.

Graph RAG is off by default. Enable GRAPH_RETRIEVAL_ENABLED=true for demos where
multi-hop context across assets, work orders, and policies improves answer quality
(e.g., the Chiller 3 scenario where WO history, manual diagnosis steps, and warranty
policy all need to be surfaced together).

LangSmith eval dataset (chiller-rag-eval) becomes the ground truth for routing
accuracy, groundedness, and cost-per-request regressions. Phase 3 CI gate will
fail builds that exceed the MAX_COST_PER_REQUEST_USD threshold on the eval set.

The FalconRetriever is the canonical retrieval path in HYBRID and CLOUD modes.
Switching from Pinecone to Azure AI Search in the future requires only a new
_cloud_retrieve() method, not changes to agent code or the supervisor graph.
