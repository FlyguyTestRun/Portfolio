"""Redis client wrapper. Handles connection errors gracefully so the
application degrades to cache-miss behavior when Redis is unavailable."""

from __future__ import annotations

import warnings

from falcon_grounds.config import REDIS_URL


class RedisClient:
    """Thin wrapper around redis.Redis with graceful error handling."""

    def __init__(self) -> None:
        self._client = None
        if not REDIS_URL:
            return
        try:
            import redis
            self._client = redis.Redis.from_url(REDIS_URL, decode_responses=False)
        except Exception as exc:
            warnings.warn(f"Redis not available: {exc}.", stacklevel=2)

    def get(self, key: str) -> bytes | None:
        if self._client is None:
            return None
        try:
            return self._client.get(key)
        except Exception:
            return None

    def set(self, key: str, value: str, ex: int | None = None) -> bool:
        if self._client is None:
            return False
        try:
            self._client.set(key, value, ex=ex)
            return True
        except Exception:
            return False

    def setex(self, key: str, seconds: int, value: str) -> bool:
        if self._client is None:
            return False
        try:
            self._client.setex(key, seconds, value)
            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        if self._client is None:
            return False
        try:
            self._client.delete(key)
            return True
        except Exception:
            return False

    def ping(self) -> bool:
        if self._client is None:
            return False
        try:
            return bool(self._client.ping())
        except Exception:
            return False


_redis_instance: RedisClient | None = None


def get_redis_client() -> RedisClient:
    global _redis_instance
    if _redis_instance is None:
        _redis_instance = RedisClient()
    return _redis_instance
