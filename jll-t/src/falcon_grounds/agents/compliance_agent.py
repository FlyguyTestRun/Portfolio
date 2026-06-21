"""Compliance agent. Assesses confidence in the retrieved context, checks for
warranty and policy constraints, and determines whether HITL review is required."""

from __future__ import annotations

import json

from falcon_grounds.config import CONFIDENCE_HITL_THRESHOLD, RUNTIME_MODE, RuntimeMode
from falcon_grounds.governance.confidence import score_confidence
from falcon_grounds.graph.state import AgentState, add_cost
from falcon_grounds.llm.clients import get_llm_client

COMPLIANCE_COST_STUB_USD = 0.0  # Local stub incurs no model cost.


def run_compliance(state: AgentState) -> AgentState:
    """Score confidence, check compliance constraints, and set requires_hitl."""
    state = dict(state)
    chunks = state.get("retrieval_chunks", [])
    query = state.get("query", "")

    if RUNTIME_MODE == RuntimeMode.LOCAL:
        confidence_score = 0.88
        compliance_evidence = [
            "Service manual confirms high head pressure typically indicates refrigerant "
            "charge issue or condenser fouling.",
            "Warranty document: 5-year coverage active through 2029-03-15. Compressor "
            "replacement is covered under the manufacturer warranty.",
        ]
        policy_flags: list[str] = []
        requires_hitl = False
        cost = COMPLIANCE_COST_STUB_USD
    else:
        llm = get_llm_client()
        chunk_text = "\n\n".join(c.get("content", "") for c in chunks)
        prompt = (
            f"Query: {query}\n\nContext:\n{chunk_text}\n\n"
            "Respond with JSON: {confidence_score, evidence, policy_flags, requires_hitl}"
        )
        raw, cost = llm.complete(prompt, task_type="compliance")
        try:
            parsed = json.loads(raw)
            confidence_score = float(parsed.get("confidence_score", 0.5))
            compliance_evidence = parsed.get("evidence", [])
            policy_flags = parsed.get("policy_flags", [])
            requires_hitl = bool(parsed.get("requires_hitl", False))
        except Exception:
            confidence_score = 0.5
            compliance_evidence = []
            policy_flags = []
            requires_hitl = True

    if not requires_hitl and confidence_score < CONFIDENCE_HITL_THRESHOLD:
        requires_hitl = True

    state["confidence_score"] = confidence_score
    state["compliance_evidence"] = compliance_evidence
    state["policy_flags"] = policy_flags
    state["requires_hitl"] = requires_hitl

    state = add_cost(state, "compliance", cost)
    return state
