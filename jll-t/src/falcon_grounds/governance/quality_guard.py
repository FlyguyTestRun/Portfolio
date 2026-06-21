"""Groundedness guard. Verifies that key terms in the answer appear in the
retrieved context. Ungrounded answers are flagged for retry or escalation."""

from __future__ import annotations


def check_groundedness(answer: str, chunks: list[dict]) -> tuple[bool, str]:
    """Return (grounded, reason).

    An answer is considered grounded if at least 40% of its key terms (words
    longer than 4 characters) appear in the combined text of the retrieved chunks.

    Edge cases:
    - Empty answer: fails with explanation.
    - No chunks: fails with explanation.
    - Answer with no extractable key terms: passes (nothing to verify).
    """
    if not answer:
        return (False, "Empty answer.")

    if not chunks:
        return (False, "No retrieval chunks to ground answer against.")

    key_terms = [w.lower() for w in answer.split() if len(w) > 4]
    if not key_terms:
        return (True, "Answer has no extractable key terms. Passing groundedness check.")

    combined = " ".join(c.get("content", "") for c in chunks).lower()
    matching = sum(1 for term in key_terms if term in combined)
    overlap = matching / len(key_terms)

    if overlap >= 0.40:
        return (True, f"Answer is grounded. {overlap:.0%} of key terms found in retrieval context.")
    return (False, f"Answer may not be grounded. Only {overlap:.0%} of key terms found in retrieval context.")
