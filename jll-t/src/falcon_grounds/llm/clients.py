"""LLM client abstraction. Selects between Azure OpenAI and a local stub based on
RUNTIME_MODE and the presence of AZURE_OPENAI_ENDPOINT."""

from __future__ import annotations

import hashlib
import json

from falcon_grounds.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_FAST_DEPLOYMENT,
    AZURE_OPENAI_FRONTIER_DEPLOYMENT,
    RUNTIME_MODE,
    RuntimeMode,
)
from falcon_grounds.graph.model_router import route_model


class LocalStubClient:
    """Deterministic response stub for local development. No network calls."""

    def complete(self, prompt: str, task_type: str, system: str = "") -> tuple[str, float]:
        """Return a canned response appropriate for the task type."""
        t = task_type.lower()
        if t == "routing":
            return ("retrieval", 0.0)
        if t == "compliance":
            payload = {
                "confidence_score": 0.88,
                "evidence": [
                    "Service manual confirms high head pressure typically indicates refrigerant "
                    "charge issue or condenser fouling.",
                    "Warranty document: 5-year coverage active through 2029-03-15. Compressor "
                    "replacement is covered under the manufacturer warranty.",
                ],
                "policy_flags": [],
                "requires_hitl": False,
            }
            return (json.dumps(payload), 0.0)
        if t == "summarization":
            return (
                "Chiller 3 (ASSET-CHI-3A) has a documented history of high head pressure events. "
                "Work order WO-2025-1102 resolved a similar alarm in October 2025 by cleaning "
                "condenser coils. The current open work order (WO-2026-0023) reports intermittent "
                "alarms since June 18, 2026. The most likely cause is condenser coil fouling or "
                "partial refrigerant overcharge. The unit is under active Carrier warranty through "
                "2029-03-15. A preventive maintenance work order should be opened to inspect coils "
                "and verify refrigerant charge before escalating to a warranty claim.",
                0.0,
            )
        if t == "extraction":
            return (json.dumps({"extracted": True, "fields": {}}), 0.0)
        return ("Stub response for local mode.", 0.0)

    def embed(self, text: str) -> tuple[list[float], float]:
        """Return a deterministic 384-dimensional embedding derived from the text hash."""
        seed = int(hashlib.sha256(text.encode()).hexdigest()[:16], 16)
        dims = 384
        vector: list[float] = []
        for i in range(dims):
            val = ((seed * (i + 1) * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFF) / 0xFFFFFFFF
            vector.append(round(val * 2 - 1, 6))
        magnitude = sum(v * v for v in vector) ** 0.5
        if magnitude > 0:
            vector = [v / magnitude for v in vector]
        return (vector, 0.0)


class _AzureBackend:
    """Thin wrapper around the openai AzureOpenAI client."""

    def __init__(self) -> None:
        import openai
        self._client = openai.AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
        )

    def complete(self, prompt: str, task_type: str, system: str = "") -> tuple[str, float]:
        decision = route_model(task_type)
        deployment = (
            AZURE_OPENAI_FRONTIER_DEPLOYMENT if decision.tier == "frontier" else AZURE_OPENAI_FAST_DEPLOYMENT
        )
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = self._client.chat.completions.create(model=deployment, messages=messages)
        text = response.choices[0].message.content or ""
        total_tokens = response.usage.total_tokens if response.usage else 2000
        from falcon_grounds.graph.model_router import TIER_COST_PER_1K
        cost = (total_tokens / 1000) * TIER_COST_PER_1K[decision.tier]
        return (text, cost)

    def embed(self, text: str) -> tuple[list[float], float]:
        response = self._client.embeddings.create(model="text-embedding-3-small", input=text)
        vector = response.data[0].embedding
        tokens = response.usage.total_tokens if response.usage else len(text.split())
        cost = (tokens / 1000) * 0.00002
        return (vector, cost)


class LLMClient:
    """Unified LLM client that selects the appropriate backend at construction time."""

    def __init__(self) -> None:
        if RUNTIME_MODE in (RuntimeMode.HYBRID, RuntimeMode.CLOUD) and AZURE_OPENAI_ENDPOINT:
            try:
                self._backend: LocalStubClient | _AzureBackend = _AzureBackend()
            except Exception:
                self._backend = LocalStubClient()
        else:
            self._backend = LocalStubClient()

    def complete(self, prompt: str, task_type: str, system: str = "") -> tuple[str, float]:
        """Run a completion. Returns (response_text, cost_usd)."""
        return self._backend.complete(prompt, task_type, system)

    def embed(self, text: str) -> tuple[list[float], float]:
        """Generate an embedding. Returns (vector, cost_usd)."""
        return self._backend.embed(text)


_llm_instance: LLMClient | None = None


def get_llm_client() -> LLMClient:
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LLMClient()
    return _llm_instance
