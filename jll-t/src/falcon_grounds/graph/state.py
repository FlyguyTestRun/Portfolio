"""Typed state schema for the falcon-grounds agent graph."""

from __future__ import annotations

import uuid
from typing import Literal, Optional, TypedDict


class AgentState(TypedDict):
    query: str
    asset_id: Optional[str]
    tenant_id: str
    run_id: str
    route: Literal["deterministic", "cached", "agent", "hitl", "error"]
    routing_rationale: str
    model_tier: Literal["frontier", "fast", "none"]
    retrieval_chunks: list[dict]
    retrieval_sources: list[str]
    retrieval_store: str
    retrieval_cost_usd: float
    confidence_score: float
    compliance_evidence: list[str]
    policy_flags: list[str]
    requires_hitl: bool
    proposed_action: str
    work_order_id: Optional[str]
    idempotency_key: str
    committed: bool
    answer: str
    grounded: bool
    hitl_pending: bool
    hitl_decision: Literal["approved", "rejected", "pending"]
    cost_layers: dict[str, float]
    total_cost_usd: float
    iteration: int
    error: Optional[str]


def default_state() -> AgentState:
    """Return a new AgentState with safe default values."""
    return AgentState(
        query="",
        asset_id=None,
        tenant_id="meridian",
        run_id=str(uuid.uuid4())[:8],
        route="agent",
        routing_rationale="",
        model_tier="none",
        retrieval_chunks=[],
        retrieval_sources=[],
        retrieval_store="",
        retrieval_cost_usd=0.0,
        confidence_score=0.0,
        compliance_evidence=[],
        policy_flags=[],
        requires_hitl=False,
        proposed_action="",
        work_order_id=None,
        idempotency_key="",
        committed=False,
        answer="",
        grounded=False,
        hitl_pending=False,
        hitl_decision="pending",
        cost_layers={},
        total_cost_usd=0.0,
        iteration=0,
        error=None,
    )


def add_cost(state: dict, layer: str, cost_usd: float) -> dict:
    """Add a cost entry to state and update the running total. Returns updated state dict."""
    layers = dict(state.get("cost_layers", {}))
    layers[layer] = layers.get(layer, 0.0) + cost_usd
    state = dict(state)
    state["cost_layers"] = layers
    state["total_cost_usd"] = state.get("total_cost_usd", 0.0) + cost_usd
    return state
