"""Handoff utilities for passing context between graph nodes."""

from __future__ import annotations

from falcon_grounds.graph.state import AgentState


def build_handoff_summary(state: AgentState) -> dict:
    """Return a minimal summary dict suitable for logging handoffs between nodes."""
    return {
        "run_id": state.get("run_id", ""),
        "tenant_id": state.get("tenant_id", ""),
        "route": state.get("route", ""),
        "model_tier": state.get("model_tier", "none"),
        "chunk_count": len(state.get("retrieval_chunks", [])),
        "confidence_score": state.get("confidence_score", 0.0),
        "requires_hitl": state.get("requires_hitl", False),
        "total_cost_usd": state.get("total_cost_usd", 0.0),
    }
