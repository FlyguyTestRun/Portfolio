"""
Layer 3 of the cost-control framework. Right-sizes model tier per task type.
Frontier models handle reasoning and compliance. Fast models handle extraction,
classification, and summarization. The 10x cost difference between tiers is the
primary lever for cost reduction on high-volume workloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

TASK_TIER_MAP: dict[str, str] = {
    "reasoning": "frontier",
    "compliance": "frontier",
    "routing": "frontier",
    "extraction": "fast",
    "classification": "fast",
    "summarization": "fast",
    "embedding": "fast",
}

# Blended input/output cost estimates per 1,000 tokens.
TIER_COST_PER_1K: dict[str, float] = {
    "frontier": 0.015,   # gpt-4o blended estimate
    "fast": 0.0015,      # gpt-4o-mini blended estimate
}


@dataclass
class ModelRouteDecision:
    tier: Literal["frontier", "fast"]
    rationale: str
    estimated_cost_usd: float


def route_model(task_type: str, estimated_tokens: int = 2000) -> ModelRouteDecision:
    """Return the appropriate model tier and estimated cost for a given task type.

    Unknown task types default to the fast tier to minimize cost.
    """
    tier: str = TASK_TIER_MAP.get(task_type.lower(), "fast")
    cost = (estimated_tokens / 1000) * TIER_COST_PER_1K[tier]

    if tier == "frontier":
        rationale = (
            f"Task type '{task_type}' requires frontier reasoning capability. "
            f"Estimated {estimated_tokens} tokens at ${TIER_COST_PER_1K[tier]}/1K = ${cost:.5f}."
        )
    else:
        rationale = (
            f"Task type '{task_type}' is handled by fast tier. "
            f"Estimated {estimated_tokens} tokens at ${TIER_COST_PER_1K[tier]}/1K = ${cost:.5f}."
        )

    return ModelRouteDecision(tier=tier, rationale=rationale, estimated_cost_usd=cost)  # type: ignore[arg-type]
