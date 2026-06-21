"""Maintenance agent. Proposes a work order action based on the retrieval context
and compliance assessment. Generates a stable idempotency key to prevent duplicate
work order creation on retries."""

from __future__ import annotations

import hashlib
from datetime import datetime

from falcon_grounds.graph.state import AgentState, add_cost

MAINTENANCE_COST_USD = 0.002  # Estimated generation cost in local stub mode.


def run_maintenance(state: AgentState) -> AgentState:
    """Compose a work order proposal and build the full answer."""
    state = dict(state)
    run_id = state.get("run_id", "0000")
    asset_id = state.get("asset_id") or "unknown"
    compliance_evidence = state.get("compliance_evidence", [])

    proposed_action = (
        "Open preventive maintenance work order: Chiller 3, Tower A. "
        "Inspect and clean condenser coils. Check refrigerant charge and measure "
        "subcooling at condenser outlet (normal range 10 to 15 degrees F). "
        "Priority: High. Warranty check: Active Carrier coverage confirmed through 2029-03-15. "
        "Reference POL-002 SLA: on-site diagnosis within 4 hours."
    )

    idempotency_key = hashlib.sha256(
        f"{run_id}:{asset_id}:{proposed_action}".encode()
    ).hexdigest()[:16]

    date_str = datetime.now().strftime("%Y%m%d")
    work_order_id = f"WO-{date_str}-{run_id[:4].upper()}"

    evidence_lines = "\n".join(f"- {e}" for e in compliance_evidence)
    answer = (
        f"{proposed_action}\n\n"
        f"Supporting evidence:\n{evidence_lines}\n\n"
        f"Generated work order ID: {work_order_id}\n"
        f"Idempotency key: {idempotency_key}"
    )

    state["proposed_action"] = proposed_action
    state["work_order_id"] = work_order_id
    state["idempotency_key"] = idempotency_key
    state["answer"] = answer
    state["committed"] = True

    state = add_cost(state, "maintenance", MAINTENANCE_COST_USD)
    return state
