"""Tests for confidence scoring."""

import pytest

from falcon_grounds.governance.confidence import score_confidence


def test_score_between_zero_and_one_with_good_inputs() -> None:
    chunks = [
        {"source": "manuals", "content": "High head pressure is caused by condenser fouling."},
        {"source": "work_orders", "content": "Cleaned condenser coils. Pressure normal."},
        {"source": "policies", "content": "Chiller units are critical infrastructure."},
    ]
    answer = "The chiller is experiencing high head pressure due to condenser coil fouling based on previous work order history and manufacturer guidance."
    score, evidence = score_confidence("chiller high head pressure", chunks, answer)
    assert 0.0 <= score <= 1.0
    assert len(evidence) > 0


def test_empty_chunks_gives_low_score() -> None:
    score, evidence = score_confidence("chiller status", [], "The chiller is fine.")
    assert score < 0.5


def test_empty_answer_gives_low_score() -> None:
    chunks = [{"source": "manuals", "content": "Chiller maintenance data."}]
    score, evidence = score_confidence("chiller", chunks, "")
    assert score < 0.5


def test_rich_context_gives_high_score() -> None:
    chunks = [
        {"source": "manuals", "content": " ".join(["chiller"] * 50)},
        {"source": "work_orders", "content": " ".join(["pressure"] * 50)},
        {"source": "policies", "content": " ".join(["warranty"] * 50)},
    ]
    answer = " ".join(["chiller condenser pressure warranty maintenance"] * 20)
    score, _ = score_confidence("chiller", chunks, answer)
    assert score >= 0.9


def test_single_source_lowers_diversity_component() -> None:
    chunks_single = [
        {"source": "manuals", "content": "Chiller data."},
        {"source": "manuals", "content": "More chiller data."},
    ]
    chunks_multi = [
        {"source": "manuals", "content": "Chiller data."},
        {"source": "work_orders", "content": "Work order data."},
    ]
    answer = " ".join(["maintenance"] * 30)
    score_single, _ = score_confidence("chiller", chunks_single, answer)
    score_multi, _ = score_confidence("chiller", chunks_multi, answer)
    assert score_multi > score_single


def test_evidence_explains_all_components() -> None:
    chunks = [{"source": "manuals", "content": "Chiller info."}]
    answer = "The chiller needs maintenance."
    _, evidence = score_confidence("chiller", chunks, answer)
    combined = " ".join(evidence).lower()
    assert "coverage" in combined or "chunk" in combined
    assert "answer" in combined or "word" in combined
    assert "total" in combined
