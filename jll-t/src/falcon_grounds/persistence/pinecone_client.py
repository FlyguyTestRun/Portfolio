"""Pinecone vector store client. In local mode, this client is intentionally
unavailable. Set RUNTIME_MODE=hybrid or cloud with a valid PINECONE_API_KEY
to enable vector search."""

from __future__ import annotations

from falcon_grounds.config import PINECONE_API_KEY, PINECONE_INDEX_NAME, RUNTIME_MODE, RuntimeMode

_NOT_AVAILABLE_MSG = (
    "Pinecone requires RUNTIME_MODE=hybrid or cloud and a valid PINECONE_API_KEY."
)


class PineconeClient:
    """Pinecone upsert and query client."""

    def __init__(self) -> None:
        self._available = False
        self._index = None
        if RUNTIME_MODE == RuntimeMode.LOCAL:
            return
        if not PINECONE_API_KEY:
            return
        try:
            from pinecone import Pinecone
            pc = Pinecone(api_key=PINECONE_API_KEY)
            self._index = pc.Index(PINECONE_INDEX_NAME)
            self._available = True
        except Exception:
            pass

    def upsert(self, vectors: list[dict], namespace: str) -> None:
        if not self._available or self._index is None:
            raise NotImplementedError(_NOT_AVAILABLE_MSG)
        self._index.upsert(vectors=vectors, namespace=namespace)

    def query(self, vector: list[float], top_k: int, namespace: str) -> list[dict]:
        if not self._available or self._index is None:
            raise NotImplementedError(_NOT_AVAILABLE_MSG)
        result = self._index.query(vector=vector, top_k=top_k, namespace=namespace, include_metadata=True)
        return result.get("matches", [])


_pinecone_instance: PineconeClient | None = None


def get_pinecone_client() -> PineconeClient:
    global _pinecone_instance
    if _pinecone_instance is None:
        _pinecone_instance = PineconeClient()
    return _pinecone_instance
