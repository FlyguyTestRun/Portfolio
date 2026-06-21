"""LangChain-native retriever wrapping falcon-grounds hybrid retrieval.

Exposes BaseRetriever so LangSmith traces retrieval as a first-class span
and so the vector backend can be swapped via RUNTIME_MODE without touching
agent code. Returns List[Document] (LangChain schema).

Dispatch:
  LOCAL  -> PostgreSQL keyword search via pg_client (no cloud deps)
  HYBRID -> langchain-postgres PGVector
  CLOUD  -> langchain-pinecone PineconeVectorStore
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import Field

import falcon_grounds.config as cfg
from falcon_grounds.config import RuntimeMode


class FalconRetriever(BaseRetriever):
    """Retriever that dispatches to PGVector (local/hybrid) or Pinecone (cloud)."""

    tenant_id: str = Field(default="meridian")
    top_k: int = Field(default=5)

    def _get_relevant_documents(self, query: str) -> List[Document]:  # type: ignore[override]
        if cfg.RUNTIME_MODE == RuntimeMode.LOCAL:
            return self._local_retrieve(query)
        elif cfg.RUNTIME_MODE == RuntimeMode.HYBRID:
            return self._pgvector_retrieve(query)
        return self._pinecone_retrieve(query)

    def _local_retrieve(self, query: str) -> List[Document]:
        from falcon_grounds.persistence.pg_client import PgClient  # type: ignore[import]

        pg = PgClient()
        if not pg.available:
            return []
        keywords = [w.lower() for w in query.split() if len(w) > 3]
        chunks = pg.keyword_search(keywords, tenant_id=self.tenant_id, top_k=self.top_k)
        return [
            Document(
                page_content=c.get("content", ""),
                metadata={
                    "source": c.get("source", ""),
                    "id": c.get("id", ""),
                    "score": c.get("score", 0.0),
                },
            )
            for c in chunks
        ]

    def _pgvector_retrieve(self, query: str) -> List[Document]:
        try:
            from langchain_openai import AzureOpenAIEmbeddings  # type: ignore[import-untyped]
            from langchain_postgres import PGVector  # type: ignore[import-untyped]

            embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=cfg.AZURE_OPENAI_ENDPOINT,
                api_key=cfg.AZURE_OPENAI_API_KEY,
                api_version=cfg.AZURE_OPENAI_API_VERSION,
            )
            store = PGVector(
                embeddings=embeddings,
                collection_name=f"tenant_{self.tenant_id}",
                connection=cfg.DATABASE_URL,
            )
            return store.similarity_search(query, k=self.top_k)
        except Exception:
            return self._local_retrieve(query)

    def _pinecone_retrieve(self, query: str) -> List[Document]:
        try:
            from langchain_openai import AzureOpenAIEmbeddings  # type: ignore[import-untyped]
            from langchain_pinecone import PineconeVectorStore  # type: ignore[import-untyped]
            from pinecone import Pinecone  # type: ignore[import-untyped]

            pc = Pinecone(api_key=cfg.PINECONE_API_KEY)
            index = pc.Index(cfg.PINECONE_INDEX_NAME)
            embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=cfg.AZURE_OPENAI_ENDPOINT,
                api_key=cfg.AZURE_OPENAI_API_KEY,
                api_version=cfg.AZURE_OPENAI_API_VERSION,
            )
            store = PineconeVectorStore(
                index=index,
                embedding=embeddings,
                namespace=f"tenant_{self.tenant_id}",
            )
            return store.similarity_search(query, k=self.top_k)
        except Exception:
            return self._local_retrieve(query)
