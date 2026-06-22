"""LangGraph StateGraph supervisor. Orchestrates the seven-layer cost-control
pipeline from deterministic pre-routing through retrieval, compliance,
maintenance, quality guard, and HITL to final cost recording."""

from __future__ import annotations

import uuid

from langgraph.graph import END, StateGraph

from falcon_grounds.agents.compliance_agent import run_compliance
from falcon_grounds.agents.maintenance_agent import run_maintenance
from falcon_grounds.agents.retrieval_agent import run_retrieval
from falcon_grounds.config import CONFIDENCE_AUTO_THRESHOLD, CONFIDENCE_HITL_THRESHOLD, GRAPH_RETRIEVAL_ENABLED
from falcon_grounds.governance.audit import log_event
from falcon_grounds.governance.hitl import request_hitl_approval
from falcon_grounds.governance.quality_guard import check_groundedness
from falcon_grounds.graph.model_router import route_model
from falcon_grounds.graph.pre_router import pre_route
from falcon_grounds.graph.state import AgentState, add_cost, default_state
from falcon_grounds.observability.cost_attribution import record_cost_entry
from falcon_grounds.rag.graph_retriever import FacilitiesGraphRetriever

_graph_retriever = FacilitiesGraphRetriever()


# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------

def node_pre_router(state: AgentState) -> AgentState:
    """Layer 1: deterministic routing via regex pattern matching."""
    state = dict(state)
    result = pre_route(state)  # type: ignore[arg-type]
    if result.resolved:
        state["route"] = "deterministic"
        state["routing_rationale"] = result.rationale
        state["answer"] = (
            f"Deterministic route: {result.action} for parameters {result.params}. "
            "No model call required."
        )
    else:
        state["route"] = "agent"
        state["routing_rationale"] = result.rationale
    log_event(state["run_id"], state["tenant_id"], "pre_router", {"route": state["route"], "rationale": state["routing_rationale"]})
    return state  # type: ignore[return-value]


def node_supervisor(state: AgentState) -> AgentState:
    """Select model tier and log the routing decision."""
    state = dict(state)
    decision = route_model("routing", estimated_tokens=500)
    state["model_tier"] = decision.tier  # type: ignore[typeddict-item]
    state = add_cost(state, "supervisor", decision.estimated_cost_usd)
    log_event(state["run_id"], state["tenant_id"], "supervisor", {"tier": decision.tier, "rationale": decision.rationale})
    return state  # type: ignore[return-value]


def node_retrieval(state: AgentState) -> AgentState:
    """Retrieve and rank relevant context from the knowledge base."""
    result = run_retrieval(state)  # type: ignore[arg-type]
    if GRAPH_RETRIEVAL_ENABLED and result.get("retrieval_chunks"):
        result = dict(result)
        result["retrieval_chunks"] = _graph_retriever.enrich(result["retrieval_chunks"])
    log_event(result["run_id"], result["tenant_id"], "retrieval", {"chunk_count": len(result["retrieval_chunks"]), "sources": result["retrieval_sources"]})
    return result  # type: ignore[return-value]


def node_compliance(state: AgentState) -> AgentState:
    """Assess confidence and check compliance constraints."""
    result = run_compliance(state)  # type: ignore[arg-type]
    log_event(result["run_id"], result["tenant_id"], "compliance", {"confidence_score": result["confidence_score"], "requires_hitl": result["requires_hitl"]})
    return result  # type: ignore[return-value]


def node_maintenance(state: AgentState) -> AgentState:
    """Propose a maintenance action and compose the answer."""
    result = run_maintenance(state)  # type: ignore[arg-type]
    log_event(result["run_id"], result["tenant_id"], "maintenance", {"work_order_id": result.get("work_order_id"), "proposed_action": result.get("proposed_action", "")[:80]})
    return result  # type: ignore[return-value]


def node_quality_guard(state: AgentState) -> AgentState:
    """Verify answer groundedness. Ungrounded answers re-enter retrieval."""
    state = dict(state)
    grounded, reason = check_groundedness(state.get("answer", ""), state.get("retrieval_chunks", []))
    state["grounded"] = grounded
    state["iteration"] = state.get("iteration", 0) + 1
    log_event(state["run_id"], state["tenant_id"], "quality_guard", {"grounded": grounded, "reason": reason, "iteration": state["iteration"]})
    return state  # type: ignore[return-value]


def node_hitl(state: AgentState) -> AgentState:
    """Pause for human review. In local mode this is a console prompt."""
    state = dict(state)
    decision = request_hitl_approval(state)  # type: ignore[arg-type]
    state["hitl_decision"] = decision  # type: ignore[typeddict-item]
    state["hitl_pending"] = False
    state["route"] = "hitl"

    if not state.get("answer"):
        state["answer"] = (
            f"HITL decision: {decision}. "
            f"Proposed action: {state.get('proposed_action', 'none')}."
        )
    log_event(state["run_id"], state["tenant_id"], "hitl", {"decision": decision})
    return state  # type: ignore[return-value]


def node_record_cost(state: AgentState) -> AgentState:
    """Layer 7: write cost entry and close the audit trail."""
    state = dict(state)
    record_cost_entry(state)  # type: ignore[arg-type]
    log_event(state["run_id"], state["tenant_id"], "record_cost", {"total_cost_usd": state.get("total_cost_usd", 0.0), "route": state.get("route", "")})
    return state  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Routing functions
# ---------------------------------------------------------------------------

def route_after_pre_router(state: AgentState) -> str:
    if state.get("route") == "deterministic":
        return "record_cost"
    return "supervisor"


def route_after_compliance(state: AgentState) -> str:
    if state.get("requires_hitl") or state.get("confidence_score", 0.0) < CONFIDENCE_HITL_THRESHOLD:
        return "hitl"
    if state.get("confidence_score", 0.0) >= CONFIDENCE_AUTO_THRESHOLD:
        return "maintenance"
    return "hitl"


def route_after_quality_guard(state: AgentState) -> str:
    if state.get("grounded"):
        return "record_cost"
    # Only retry retrieval if the previous pass returned chunks. Retrying against
    # an empty retrieval store is a no-op and wastes per-call cost budget.
    if state.get("iteration", 0) < 3 and state.get("retrieval_chunks"):
        return "retrieval"
    return "record_cost"


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def create_compiled_graph():  # type: ignore[return]
    """Build and compile the LangGraph StateGraph."""
    graph: StateGraph = StateGraph(AgentState)

    graph.add_node("pre_router", node_pre_router)
    graph.add_node("supervisor", node_supervisor)
    graph.add_node("retrieval", node_retrieval)
    graph.add_node("compliance", node_compliance)
    graph.add_node("maintenance", node_maintenance)
    graph.add_node("quality_guard", node_quality_guard)
    graph.add_node("hitl", node_hitl)
    graph.add_node("record_cost", node_record_cost)

    graph.set_entry_point("pre_router")

    graph.add_conditional_edges(
        "pre_router",
        route_after_pre_router,
        {"record_cost": "record_cost", "supervisor": "supervisor"},
    )
    graph.add_edge("supervisor", "retrieval")
    graph.add_edge("retrieval", "compliance")
    graph.add_conditional_edges(
        "compliance",
        route_after_compliance,
        {"hitl": "hitl", "maintenance": "maintenance"},
    )
    graph.add_edge("maintenance", "quality_guard")
    graph.add_conditional_edges(
        "quality_guard",
        route_after_quality_guard,
        {"record_cost": "record_cost", "retrieval": "retrieval"},
    )
    graph.add_edge("hitl", "record_cost")
    graph.add_edge("record_cost", END)

    return graph.compile()


def run_query(query: str, tenant_id: str = "meridian", asset_id: str | None = None) -> AgentState:
    """Run the full agent graph for a query and return the final state."""
    state = default_state()
    state["query"] = query
    state["tenant_id"] = tenant_id
    state["run_id"] = str(uuid.uuid4())[:8]
    state["asset_id"] = asset_id

    compiled = create_compiled_graph()
    result = compiled.invoke(state)
    return result  # type: ignore[return-value]
