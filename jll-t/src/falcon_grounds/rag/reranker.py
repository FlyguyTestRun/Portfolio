"""Cross-encoder reranker. In local mode, sorts by pre-computed score.
In production, this would call a dedicated cross-encoder model or a
managed reranking API to produce more accurate relevance scores."""

from __future__ import annotations


def rerank(query: str, chunks: list[dict], top_k: int = 3) -> list[dict]:
    """Rerank retrieved chunks by relevance to the query.

    Local mode uses the score already assigned by the retriever. A production
    deployment would replace this with a cross-encoder pass (e.g., Cohere
    Rerank or a self-hosted sentence-transformers cross-encoder).
    """
    sorted_chunks = sorted(chunks, key=lambda c: c.get("score", 0.0), reverse=True)
    return sorted_chunks[:top_k]
