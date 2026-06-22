"""Retrieval agent. Queries PostgreSQL for assets, work orders, policies, and
service manuals relevant to the current query. Applies keyword matching in
local mode and vector search in hybrid/cloud mode."""

from __future__ import annotations

from falcon_grounds.graph.state import AgentState, add_cost
from falcon_grounds.rag.hybrid_retriever import retrieve
from falcon_grounds.rag.reranker import rerank
from falcon_grounds.rag.compress import compress_context

RETRIEVAL_COST_USD = 0.001  # Estimated DB query cost per request.


def run_retrieval(state: AgentState) -> AgentState:
    """Populate state with ranked, compressed retrieval chunks."""
    state = dict(state)
    tenant_id = state.get("tenant_id", "meridian")
    query = state.get("query", "")

    raw_chunks = retrieve(query, tenant_id, top_k=10)
    ranked = rerank(query, raw_chunks, top_k=5)
    compressed = compress_context(ranked, max_tokens=2000)

    sources = list(dict.fromkeys(c.get("source", "") for c in compressed))

    state["retrieval_chunks"] = compressed
    state["retrieval_sources"] = sources
    state["retrieval_store"] = "pgvector"
    state["retrieval_cost_usd"] = RETRIEVAL_COST_USD

    state = add_cost(state, "retrieval", RETRIEVAL_COST_USD)
    return state
