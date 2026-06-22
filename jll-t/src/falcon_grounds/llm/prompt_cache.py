"""
Layer 4 of the cost-control framework. Provider-native prompt caching. Stable system
prompts are cached at the provider level, reducing input token charges by up to 90%
on repeated calls. Prompts are built once, stored in-process, and structured to
maximize cached-prefix utilization.
"""

from __future__ import annotations

SYSTEM_PROMPTS: dict[str, str] = {
    "facilities_analyst": (
        "You are a senior facilities management analyst with expertise in commercial real estate "
        "operations, HVAC systems, and predictive maintenance. You analyze equipment data, work "
        "order history, and service manuals to provide accurate, actionable assessments. "
        "You cite specific data points and flag any uncertainty."
    ),
    "compliance_checker": (
        "You are a compliance and warranty specialist for commercial facilities. You review "
        "equipment maintenance records, warranty documentation, and regulatory policies to "
        "identify constraints on proposed maintenance actions. You flag any action that could "
        "void warranties or create compliance risk."
    ),
    "work_order_creator": (
        "You are a facilities operations coordinator responsible for creating precise, actionable "
        "work orders. Work orders must include: affected asset ID, issue description, priority "
        "level, required skills, estimated duration, warranty status, and any safety precautions."
    ),
}


class PromptCache:
    """In-process cache for stable system prompts.

    Prompts are placed at the front of the message list and remain unchanged
    across calls, which maximizes provider-side cached-prefix hits.
    """

    def __init__(self) -> None:
        self._cache: dict[str, str] = {}

    def get_system_prompt(self, role: str) -> str:
        """Return the system prompt for a given role, building it once and caching it."""
        if role not in self._cache:
            self._cache[role] = SYSTEM_PROMPTS.get(role, SYSTEM_PROMPTS["facilities_analyst"])
        return self._cache[role]


_cache_instance: PromptCache | None = None


def get_prompt_cache() -> PromptCache:
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = PromptCache()
    return _cache_instance
