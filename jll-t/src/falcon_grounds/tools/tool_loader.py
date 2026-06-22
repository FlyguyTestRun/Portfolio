"""
Layer 6 of the cost-control framework. Tool-context discipline. Only the tools
required for the current step are loaded into the model context. Loading the full
tool catalog on every call multiplies input tokens proportionally to catalog size.
With a 10-tool catalog, this pattern reduces tool-definition tokens by 70 to 80
percent per step.
"""

from __future__ import annotations

STEP_TOOL_MAP: dict[str, list[str]] = {
    "retrieval": ["search_assets", "search_work_orders", "search_manuals"],
    "compliance": ["check_policy", "check_warranty"],
    "maintenance": ["create_work_order", "update_asset_status"],
    "supervisor": ["route_to_retrieval", "route_to_compliance", "route_to_maintenance"],
}


def load_tools_for_step(step_name: str) -> list[str]:
    """Return the tool names available for a given graph step.

    Returns an empty list for unknown step names, which prevents accidental
    tool-catalog inflation from unregistered steps.
    """
    return STEP_TOOL_MAP.get(step_name, [])
