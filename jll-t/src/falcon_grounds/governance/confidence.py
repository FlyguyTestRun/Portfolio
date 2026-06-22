"""Confidence scoring for agent answers based on retrieval coverage and answer quality."""

from __future__ import annotations

from falcon_grounds.config import CONFIDENCE_AUTO_THRESHOLD, CONFIDENCE_HITL_THRESHOLD

AUTO_THRESHOLD: float = CONFIDENCE_AUTO_THRESHOLD
HITL_THRESHOLD: float = CONFIDENCE_HITL_THRESHOLD


def score_confidence(query: str, chunks: list[dict], answer: str) -> tuple[float, list[str]]:
    """Score answer confidence on a 0.0 to 1.0 scale.

    Three components:
    - Source coverage (0.4 weight): how many chunks are available, up to 3.
    - Answer adequacy (0.3 weight): word count relative to a 50-word baseline.
    - Source diversity (0.3 weight): whether more than one source table contributed.

    Returns (score, evidence_list).
    """
    evidence: list[str] = []

    source_coverage = min(len(chunks) / 3, 1.0) * 0.4
    evidence.append(
        f"Source coverage: {len(chunks)} chunk(s) retrieved "
        f"(component score: {source_coverage:.3f} / 0.4)."
    )

    answer_words = len(answer.split())
    answer_adequacy = min(answer_words / 50, 1.0) * 0.3
    evidence.append(
        f"Answer adequacy: {answer_words} words "
        f"(component score: {answer_adequacy:.3f} / 0.3)."
    )

    unique_sources = set(c.get("source", "") for c in chunks)
    diversity_factor = 1.0 if len(unique_sources) > 1 else 0.5
    source_diversity = diversity_factor * 0.3
    evidence.append(
        f"Source diversity: {len(unique_sources)} distinct source(s) "
        f"(component score: {source_diversity:.3f} / 0.3)."
    )

    score = round(source_coverage + answer_adequacy + source_diversity, 3)
    evidence.append(f"Total confidence score: {score:.3f}.")

    return (score, evidence)
