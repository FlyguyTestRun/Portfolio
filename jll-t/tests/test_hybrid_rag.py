"""Tests for the hybrid retriever with mocked PostgreSQL client."""

from __future__ import annotations

import pytest

import falcon_grounds.rag.hybrid_retriever as retriever_module
from falcon_grounds.rag.hybrid_retriever import retrieve

SAMPLE_ASSETS = [
    {"id": "ASSET-CHI-3A", "tenant_id": "meridian", "name": "Chiller 3", "type": "chiller", "location": "Tower A", "metadata": {}},
]
SAMPLE_WORK_ORDERS = [
    {"id": "WO-2026-0023", "tenant_id": "meridian", "asset_id": "ASSET-CHI-3A", "status": "open", "description": "High head pressure alarm.", "priority": "high", "metadata": {}},
    {"id": "WO-2025-1102", "tenant_id": "meridian", "asset_id": "ASSET-CHI-3A", "status": "closed", "description": "Cleaned condenser coils. Pressure returned to normal.", "priority": "high", "metadata": {}},
]
SAMPLE_POLICIES = [
    {"id": "POL-001", "tenant_id": "meridian", "name": "Warranty Claim Procedure", "content": "All repairs under warranty must be reported within 24 hours.", "category": "warranty"},
]
SAMPLE_MANUALS = [
    {"id": "MAN-001", "tenant_id": "meridian", "asset_type": "chiller", "title": "Carrier 30XA: High Head Pressure", "content": "High head pressure is caused by condenser fouling or refrigerant overcharge."},
]


@pytest.fixture
def mock_pg(monkeypatch: pytest.MonkeyPatch) -> None:
    import falcon_grounds.rag.hybrid_retriever as hr
    import falcon_grounds.persistence.pg_client as pg

    monkeypatch.setattr(pg, "query_all_assets", lambda tenant_id: SAMPLE_ASSETS)
    monkeypatch.setattr(pg, "query_all_work_orders", lambda tenant_id: SAMPLE_WORK_ORDERS)
    monkeypatch.setattr(pg, "query_policies", lambda tenant_id: SAMPLE_POLICIES)
    monkeypatch.setattr(pg, "query_all_manuals", lambda tenant_id: SAMPLE_MANUALS)


def test_chunks_have_required_keys(mock_pg: None) -> None:
    chunks = retrieve("chiller high head pressure", "meridian")
    assert len(chunks) > 0
    for chunk in chunks:
        assert "id" in chunk
        assert "content" in chunk
        assert "source" in chunk
        assert "score" in chunk


def test_relevant_query_returns_results(mock_pg: None) -> None:
    chunks = retrieve("chiller condenser coils pressure", "meridian")
    assert len(chunks) > 0


def test_irrelevant_query_returns_fewer_results(mock_pg: None) -> None:
    relevant = retrieve("chiller condenser pressure", "meridian")
    irrelevant = retrieve("elevator maintenance", "meridian")
    assert len(relevant) >= len(irrelevant)


def test_scores_are_between_zero_and_one(mock_pg: None) -> None:
    chunks = retrieve("chiller high head pressure history", "meridian")
    for chunk in chunks:
        assert 0.0 <= chunk["score"] <= 1.0


def test_empty_query_returns_empty(mock_pg: None) -> None:
    chunks = retrieve("", "meridian")
    assert chunks == []


def test_results_sorted_by_score_descending(mock_pg: None) -> None:
    chunks = retrieve("chiller head pressure condenser", "meridian", top_k=10)
    scores = [c["score"] for c in chunks]
    assert scores == sorted(scores, reverse=True)
