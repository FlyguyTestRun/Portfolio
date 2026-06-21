"""Tests for the semantic cache (Layer 2)."""

from __future__ import annotations

import json

import pytest

from falcon_grounds.rag.semantic_cache import SemanticCache, CacheResult
from falcon_grounds.config import CACHE_TTL_STATIC, CACHE_TTL_VOLATILE


class MockRedis:
    """Dictionary-backed Redis stub for testing."""

    def __init__(self) -> None:
        self._store: dict[str, bytes] = {}
        self._ttls: dict[str, int] = {}

    def get(self, key: str) -> bytes | None:
        return self._store.get(key)

    def set(self, key: str, value: str, ex: int | None = None) -> None:
        self._store[key] = value.encode() if isinstance(value, str) else value
        if ex:
            self._ttls[key] = ex

    def setex(self, key: str, seconds: int, value: str) -> None:
        self._store[key] = value.encode() if isinstance(value, str) else value
        self._ttls[key] = seconds

    def delete(self, key: str) -> None:
        self._store.pop(key, None)
        self._ttls.pop(key, None)

    def ping(self) -> bool:
        return True


def make_embedding(seed: int = 1, dims: int = 16) -> list[float]:
    return [float(i + seed) / (dims + seed) for i in range(dims)]


def test_cache_miss_on_empty_store() -> None:
    redis = MockRedis()
    cache = SemanticCache(redis)
    embedding = make_embedding()
    result = cache.get("meridian", "What is the chiller status?", embedding)
    assert result.hit is False


def test_cache_hit_after_set() -> None:
    redis = MockRedis()
    cache = SemanticCache(redis)
    embedding = make_embedding()
    answer = "The chiller is operating normally."
    sources = ["manuals"]

    cache.set("meridian", embedding, answer, sources)
    result = cache.get("meridian", "What is the chiller maintenance history?", embedding)
    assert result.hit is True
    assert result.answer == answer
    assert result.sources == sources


def test_static_ttl_for_reference_query() -> None:
    redis = MockRedis()
    cache = SemanticCache(redis)
    ttl = cache._ttl_for_query("What does the service manual say about subcooling?")
    assert ttl == CACHE_TTL_STATIC


def test_volatile_ttl_for_status_query() -> None:
    redis = MockRedis()
    cache = SemanticCache(redis)
    ttl = cache._ttl_for_query("What is the current status of the chiller?")
    assert ttl == CACHE_TTL_VOLATILE


def test_bypass_ttl_for_work_order_status() -> None:
    redis = MockRedis()
    cache = SemanticCache(redis)
    ttl = cache._ttl_for_query("work order status for ASSET-CHI-3A")
    assert ttl == 0


def test_cache_key_consistent_for_same_embedding() -> None:
    redis = MockRedis()
    cache = SemanticCache(redis)
    emb1 = [0.1234, 0.5678, 0.9012]
    emb2 = [0.1239, 0.5672, 0.9015]  # Differs at 4th decimal: rounds to same
    key1 = cache._cache_key("meridian", emb1)
    key2 = cache._cache_key("meridian", emb2)
    assert key1 == key2


def test_cache_key_differs_for_different_tenants() -> None:
    redis = MockRedis()
    cache = SemanticCache(redis)
    emb = make_embedding()
    key1 = cache._cache_key("meridian", emb)
    key2 = cache._cache_key("acme", emb)
    assert key1 != key2
