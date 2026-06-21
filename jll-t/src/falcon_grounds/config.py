"""Configuration and environment variable loading for falcon-grounds."""

import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")


class RuntimeMode(str, Enum):
    LOCAL = "local"
    HYBRID = "hybrid"
    CLOUD = "cloud"


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _float_env(key: str, default: float) -> float:
    try:
        return float(os.environ[key])
    except (KeyError, ValueError):
        return default


def _int_env(key: str, default: int) -> int:
    try:
        return int(os.environ[key])
    except (KeyError, ValueError):
        return default


_mode_raw = _env("RUNTIME_MODE", "local").lower()
RUNTIME_MODE: RuntimeMode = RuntimeMode(_mode_raw) if _mode_raw in RuntimeMode._value2member_map_ else RuntimeMode.LOCAL

DATABASE_URL: str = _env("DATABASE_URL", "")
REDIS_URL: str = _env("REDIS_URL", "redis://localhost:6379/0")

AZURE_OPENAI_ENDPOINT: str = _env("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY: str = _env("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION: str = _env("AZURE_OPENAI_API_VERSION", "2024-02-01")
AZURE_OPENAI_FRONTIER_DEPLOYMENT: str = _env("AZURE_OPENAI_FRONTIER_DEPLOYMENT", "gpt-4o")
AZURE_OPENAI_FAST_DEPLOYMENT: str = _env("AZURE_OPENAI_FAST_DEPLOYMENT", "gpt-4o-mini")

PINECONE_API_KEY: str = _env("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME: str = _env("PINECONE_INDEX_NAME", "falcon-grounds")

COSMOS_URL: str = _env("COSMOS_URL", "")
COSMOS_KEY: str = _env("COSMOS_KEY", "")
COSMOS_DB_NAME: str = _env("COSMOS_DB_NAME", "falcon_grounds")

ANTHROPIC_API_KEY: str = _env("ANTHROPIC_API_KEY", "")

HITL_WEBHOOK_URL: str = _env("HITL_WEBHOOK_URL", "")
HITL_APPROVE_URL: str = _env("HITL_APPROVE_URL", "http://localhost:8000/webhooks/approve")
HITL_REJECT_URL: str = _env("HITL_REJECT_URL", "http://localhost:8000/webhooks/reject")

MAX_COST_PER_REQUEST_USD: float = _float_env("MAX_COST_PER_REQUEST_USD", 0.10)
CONFIDENCE_AUTO_THRESHOLD: float = _float_env("CONFIDENCE_AUTO_THRESHOLD", 0.85)
CONFIDENCE_HITL_THRESHOLD: float = _float_env("CONFIDENCE_HITL_THRESHOLD", 0.60)

CACHE_TTL_STATIC: int = _int_env("CACHE_TTL_STATIC", 604800)   # 7 days
CACHE_TTL_VOLATILE: int = _int_env("CACHE_TTL_VOLATILE", 300)  # 5 minutes

_bypass_raw = _env("CACHE_TTL_BYPASS_TAGS", "work_order_status,open_wo")
CACHE_TTL_BYPASS_TAGS: list[str] = [t.strip() for t in _bypass_raw.split(",") if t.strip()]

DEFAULT_TENANT_ID: str = _env("DEFAULT_TENANT_ID", "meridian")

# LangSmith observability
LANGCHAIN_API_KEY: str = _env("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT: str = _env("LANGCHAIN_PROJECT", "falcon-grounds")
LANGCHAIN_TRACING_V2: bool = _env("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_ENDPOINT: str = _env("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
LANGSMITH_DATASET_NAME: str = _env("LANGSMITH_DATASET_NAME", "chiller-rag-eval")

# Graph RAG
GRAPH_RETRIEVAL_ENABLED: bool = _env("GRAPH_RETRIEVAL_ENABLED", "false").lower() == "true"
GRAPH_BACKEND: str = _env("GRAPH_BACKEND", "networkx")
NEO4J_URI: str = _env("NEO4J_URI", "")
NEO4J_USERNAME: str = _env("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD: str = _env("NEO4J_PASSWORD", "")
