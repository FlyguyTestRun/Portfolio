"""Document ingestion pipeline. Stores documents in PostgreSQL and, in cloud mode,
upserts embeddings into Pinecone for vector retrieval."""

from __future__ import annotations

import hashlib


def ingest_document(tenant_id: str, doc_type: str, content: str, metadata: dict) -> str:
    """Ingest a document into the appropriate storage layer.

    Returns the generated document ID.
    """
    from falcon_grounds.persistence import pg_client

    doc_id = f"DOC-{doc_type.upper()}-{hashlib.sha256(content.encode()).hexdigest()[:8]}"

    record = {
        "id": doc_id,
        "tenant_id": tenant_id,
        "asset_type": metadata.get("asset_type", "general"),
        "title": metadata.get("title", doc_id),
        "content": content,
    }
    pg_client.insert_manual(record)
    return doc_id
