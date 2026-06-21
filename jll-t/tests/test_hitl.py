"""Tests for the HITL gate in local mode."""

from __future__ import annotations

import builtins

import pytest

from falcon_grounds.governance.hitl import format_hitl_summary, request_hitl_approval
from falcon_grounds.graph.state import default_state


def make_state_for_hitl(proposed_action: str = "Open work order for chiller inspection.") -> dict:
    s = default_state()
    s["run_id"] = "test-0001"
    s["asset_id"] = "ASSET-CHI-3A"
    s["tenant_id"] = "meridian"
    s["confidence_score"] = 0.75
    s["proposed_action"] = proposed_action
    s["compliance_evidence"] = ["Active warranty through 2029."]
    s["policy_flags"] = []
    return s


def test_approve_returns_approved(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "a")
    state = make_state_for_hitl()
    result = request_hitl_approval(state)  # type: ignore[arg-type]
    assert result == "approved"


def test_reject_returns_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "r")
    state = make_state_for_hitl()
    result = request_hitl_approval(state)  # type: ignore[arg-type]
    assert result == "rejected"


def test_empty_input_returns_approved(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "")
    state = make_state_for_hitl()
    result = request_hitl_approval(state)  # type: ignore[arg-type]
    assert result == "approved"


def test_eoferror_returns_approved(monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_eof(_prompt: str = "") -> str:
        raise EOFError

    monkeypatch.setattr(builtins, "input", raise_eof)
    state = make_state_for_hitl()
    result = request_hitl_approval(state)  # type: ignore[arg-type]
    assert result == "approved"


def test_format_hitl_summary_includes_key_fields() -> None:
    state = make_state_for_hitl("Inspect condenser coils.")
    summary = format_hitl_summary(state)  # type: ignore[arg-type]
    assert "test-0001" in summary
    assert "ASSET-CHI-3A" in summary
    assert "Inspect condenser coils." in summary
    assert "0.75" in summary
