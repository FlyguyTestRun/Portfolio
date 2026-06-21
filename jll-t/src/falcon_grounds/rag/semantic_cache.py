"""
Layer 2 of the cost-control framework. Semantic caching keyed by tenant, query
embedding, and data volatility. Static reference data cached for 7 days. Volatile
operational data cached for 5 minutes. Work order status queries bypass cache entirely.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from falcon_grounds.config import CACHE_TTL_BYPASS_TAGS, CACHE_TTL_STATIC, CACHE_TTL_VOLATILE

_VOLATILE_SIGNALS = {"status", "open", "pending", "current", "today", "live", "now"}


@dataclass
class CacheResult:
    hit: bool
    answer: str = ""
    sources: list[str] = field(default_factory=list)
    cache_key: str = ""
    ttl_used: int = 0
    cost_usd: float = 0.0


class SemanticCache:
    """Redis-backed semantic cache with per-volatility TTL selection."""

    def __init__(self, redis_client: object) -> None:
        self._redis = redis_client

    def _embedding_cost(self, text: str) -> float:
        tokens = len(text.split()) / 0.75
        return (tokens / 1000) * 0.00002

    def _cache_key(self, tenant_id: str, query_embedding: list[float]) -> str:
        rounded = tuple(round(v, 3) for v in query_embedding)
        raw = f"{tenant_id}:{rounded}"
        digest = hashlib.sha256(raw.encode()).hexdigest()
        return f"sc:{digest}"

    def _ttl_for_query(self, query: str) -> int:
        query_lower = query.lower().replace("_", " ")
        for tag in CACHE_TTL_BYPASS_TAGS:
            if tag.replace("_", " ") in query_lower:
                return 0
        tokens = set(query_lower.split())
        if tokens & _VOLATILE_SIGNALS:
            return CACHE_TTL_VOLATILE
        return CACHE_TTL_STATIC

    def get(self, tenant_id: str, query: str, query_embedding: list[float]) -> CacheResult:
        """Return a cache hit if a prior answer exists for this tenant/embedding pair."""
        embedding_cost = self._embedding_cost(query)
        cache_key = self._cache_key(tenant_id, query_embedding)
        ttl = self._ttl_for_query(query)

        if ttl == 0:
            return CacheResult(hit=False, cache_key=cache_key, ttl_used=0, cost_usd=embedding_cost)

        try:
            raw = self._redis.get(cache_key)
            if raw:
                data = json.loads(raw)
                return CacheResult(
                    hit=True,
                    answer=data.get("answer", ""),
                    sources=data.get("sources", []),
                    cache_key=cache_key,
                    ttl_used=ttl,
                    cost_usd=embedding_cost,
                )
        except Exception:
            pass

        return CacheResult(hit=False, cache_key=cache_key, ttl_used=ttl, cost_usd=embedding_cost)

    def set(self, tenant_id: str, query_embedding: list[float], answer: str, sources: list[str]) -> str:
        """Store an answer in cache. Returns the cache key used."""
        cache_key = self._cache_key(tenant_id, query_embedding)
        ttl = CACHE_TTL_STATIC
        try:
            self._redis.setex(cache_key, ttl, json.dumps({"answer": answer, "sources": sources}))
        except Exception:
            pass
        return cache_key
