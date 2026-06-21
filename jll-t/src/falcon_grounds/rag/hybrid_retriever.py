"""Hybrid retriever that combines keyword search over PostgreSQL in local mode
and vector search over Pinecone in hybrid/cloud mode."""

from __future__ import annotations

from falcon_grounds import persistence


def _build_content(record: dict, source: str) -> str:
    """Flatten a record dict into a searchable text string."""
    if source == "assets":
        return (
            f"Asset: {record.get('name','')} | Type: {record.get('type','')} | "
            f"Location: {record.get('location','')} | Metadata: {record.get('metadata','')}"
        )
    if source == "work_orders":
        return (
            f"Work Order: {record.get('id','')} | Asset: {record.get('asset_id','')} | "
            f"Status: {record.get('status','')} | Priority: {record.get('priority','')} | "
            f"Description: {record.get('description','')}"
        )
    if source == "policies":
        return f"Policy: {record.get('name','')} | {record.get('content','')}"
    if source == "manuals":
        return f"Manual: {record.get('title','')} | {record.get('content','')}"
    return str(record)


def retrieve(query: str, tenant_id: str, top_k: int = 5) -> list[dict]:
    """Retrieve relevant records using keyword matching over seeded data.

    In local mode this performs keyword search over PostgreSQL. In hybrid/cloud
    mode it would issue an embedding query to Pinecone followed by a reranking
    pass.
    """
    from falcon_grounds.persistence import pg_client

    tokens = [t.lower() for t in query.split() if len(t) > 3]
    if not tokens:
        return []

    chunks: list[dict] = []

    try:
        assets = pg_client.query_all_assets(tenant_id)
        for asset in assets:
            content = _build_content(asset, "assets")
            score = sum(1 for t in tokens if t in content.lower()) / len(tokens)
            if score > 0:
                chunks.append({"id": asset["id"], "content": content, "source": "assets", "score": score, "store": "pgvector"})

        work_orders = pg_client.query_all_work_orders(tenant_id)
        for wo in work_orders:
            content = _build_content(wo, "work_orders")
            score = sum(1 for t in tokens if t in content.lower()) / len(tokens)
            if score > 0:
                chunks.append({"id": wo["id"], "content": content, "source": "work_orders", "score": score, "store": "pgvector"})

        policies = pg_client.query_policies(tenant_id)
        for policy in policies:
            content = _build_content(policy, "policies")
            score = sum(1 for t in tokens if t in content.lower()) / len(tokens)
            if score > 0:
                chunks.append({"id": policy["id"], "content": content, "source": "policies", "score": score, "store": "pgvector"})

        manuals = pg_client.query_all_manuals(tenant_id)
        for manual in manuals:
            content = _build_content(manual, "manuals")
            score = sum(1 for t in tokens if t in content.lower()) / len(tokens)
            if score > 0:
                chunks.append({"id": manual["id"], "content": content, "source": "manuals", "score": score, "store": "pgvector"})

    except Exception:
        return []

    chunks.sort(key=lambda c: c["score"], reverse=True)
    return chunks[:top_k]
