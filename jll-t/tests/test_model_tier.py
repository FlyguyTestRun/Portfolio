"""Tests for model tier routing (Layer 3)."""

import pytest

from falcon_grounds.graph.model_router import route_model, TIER_COST_PER_1K


def test_reasoning_maps_to_frontier() -> None:
    result = route_model("reasoning")
    assert result.tier == "frontier"


def test_compliance_maps_to_frontier() -> None:
    result = route_model("compliance")
    assert result.tier == "frontier"


def test_extraction_maps_to_fast() -> None:
    result = route_model("extraction")
    assert result.tier == "fast"


def test_classification_maps_to_fast() -> None:
    result = route_model("classification")
    assert result.tier == "fast"


def test_summarization_maps_to_fast() -> None:
    result = route_model("summarization")
    assert result.tier == "fast"


def test_unknown_task_defaults_to_fast() -> None:
    result = route_model("unknown_task_xyz")
    assert result.tier == "fast"


def test_cost_estimates_are_positive() -> None:
    for task in ["reasoning", "compliance", "extraction", "classification", "summarization"]:
        result = route_model(task, estimated_tokens=1000)
        assert result.estimated_cost_usd > 0


def test_fast_tier_cheaper_than_frontier() -> None:
    frontier = route_model("reasoning", estimated_tokens=1000)
    fast = route_model("extraction", estimated_tokens=1000)
    assert fast.estimated_cost_usd < frontier.estimated_cost_usd


def test_cost_scales_with_tokens() -> None:
    small = route_model("extraction", estimated_tokens=1000)
    large = route_model("extraction", estimated_tokens=4000)
    assert large.estimated_cost_usd == pytest.approx(small.estimated_cost_usd * 4, rel=1e-6)


def test_tier_cost_constants() -> None:
    assert TIER_COST_PER_1K["frontier"] > TIER_COST_PER_1K["fast"]
