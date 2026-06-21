"""
Layer 1 of the cost-control framework. Deterministic routing via regex pattern
matching. Zero model calls. Resolves hard-coded asset identifiers, work order
references, and named policy lookups before the agent graph runs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from falcon_grounds.graph.state import AgentState

ASSET_ID_PATTERN = re.compile(r"\basset[_\s-]?id[:\s]+([A-Z0-9\-]+)", re.IGNORECASE)
# Requires structured ID: WO- prefix or purely numeric token after a delimiter.
# Prevents matching "work order should" where "SHOULD" looks like an ID.
WORK_ORDER_PATTERN = re.compile(r"\bwork\s*order[_\s-]?(?:id)?[:\s]+(WO-[A-Z0-9\-]+|\d{4}-\d+)", re.IGNORECASE)
POLICY_PATTERN = re.compile(r'\bpolicy[:\s]+"([^"]+)"', re.IGNORECASE)


@dataclass
class PreRouteResult:
    resolved: bool
    action: str = ""
    params: dict = field(default_factory=dict)
    rationale: str = ""
    cost_usd: float = 0.0


def pre_route(state: AgentState) -> PreRouteResult:
    """Attempt deterministic resolution before the agent graph runs.

    Checks, in order:
    1. Asset ID set in request context (caller already resolved the asset).
    2. Asset ID pattern in query text.
    3. Work order ID pattern in query text.
    4. Named policy reference in query text.

    Returns a PreRouteResult indicating whether a route was resolved.
    """
    query: str = state.get("query", "")
    asset_id: str | None = state.get("asset_id")

    if asset_id:
        return PreRouteResult(
            resolved=True,
            action="asset_lookup",
            params={"asset_id": asset_id},
            rationale="Asset ID provided in request context.",
        )

    match = ASSET_ID_PATTERN.search(query)
    if match:
        return PreRouteResult(
            resolved=True,
            action="asset_lookup",
            params={"asset_id": match.group(1).upper()},
            rationale=f"Matched asset ID pattern: {match.group(1)}.",
        )

    match = WORK_ORDER_PATTERN.search(query)
    if match:
        return PreRouteResult(
            resolved=True,
            action="work_order_status",
            params={"work_order_id": match.group(1).upper()},
            rationale=f"Matched work order ID pattern: {match.group(1)}.",
        )

    match = POLICY_PATTERN.search(query)
    if match:
        return PreRouteResult(
            resolved=True,
            action="policy_fetch",
            params={"policy_name": match.group(1)},
            rationale=f"Matched named policy reference: {match.group(1)}.",
        )

    return PreRouteResult(
        resolved=False,
        rationale="No deterministic pattern matched. Routing to agent graph.",
    )
