"""Tests for the deterministic pre-router (Layer 1)."""

import pytest

from falcon_grounds.graph.pre_router import pre_route
from falcon_grounds.graph.state import default_state


def make_state(query: str = "", asset_id: str | None = None) -> dict:
    s = default_state()
    s["query"] = query
    s["asset_id"] = asset_id
    return s


def test_asset_id_in_query_text() -> None:
    state = make_state(query="ASSET-ID: ASSET-CHI-3A status")
    result = pre_route(state)  # type: ignore[arg-type]
    assert result.resolved is True
    assert result.action == "asset_lookup"
    assert result.params["asset_id"] == "ASSET-CHI-3A"
    assert result.cost_usd == 0.0


def test_work_order_id_in_query_text() -> None:
    state = make_state(query="What is the status of work order WO-2026-0023?")
    result = pre_route(state)  # type: ignore[arg-type]
    assert result.resolved is True
    assert result.action == "work_order_status"
    assert "WO-2026-0023" in result.params.get("work_order_id", "").upper()


def test_work_order_no_false_positive() -> None:
    # Natural language "work order should" must not match.
    state = make_state(query="What work order should we open for Chiller 3?")
    result = pre_route(state)  # type: ignore[arg-type]
    assert result.resolved is False


def test_named_policy_in_query_text() -> None:
    state = make_state(query='Please retrieve policy: "Warranty Claim Procedure" for review.')
    result = pre_route(state)  # type: ignore[arg-type]
    assert result.resolved is True
    assert result.action == "policy_fetch"
    assert "Warranty Claim Procedure" in result.params.get("policy_name", "")


def test_natural_language_query_no_match() -> None:
    state = make_state(query="Chiller 3 in Tower A is reporting intermittent high head pressure. What should we do?")
    result = pre_route(state)  # type: ignore[arg-type]
    assert result.resolved is False
    assert result.action == ""


def test_asset_id_in_state_context() -> None:
    state = make_state(query="What is the history for this asset?", asset_id="ASSET-CHI-3A")
    result = pre_route(state)  # type: ignore[arg-type]
    assert result.resolved is True
    assert result.action == "asset_lookup"
    assert result.params["asset_id"] == "ASSET-CHI-3A"
