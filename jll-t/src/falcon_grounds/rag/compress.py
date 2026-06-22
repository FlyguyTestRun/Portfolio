"""
Layer 5 of the cost-control framework. Context compression via top-k truncation.
Reduces tokens fed to the model without sacrificing retrieval quality. Operates on
pre-ranked chunks so the most relevant content is always included first.
"""

from __future__ import annotations


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: word count * 1.3 accounts for subword tokenization."""
    return int(len(text.split()) * 1.3)


def compress_context(chunks: list[dict], max_tokens: int = 2000) -> list[dict]:
    """Return a subset of chunks whose combined token count fits within max_tokens.

    Chunks are processed in the order provided (caller is responsible for ranking
    before compressing). If a single chunk exceeds the budget, it is truncated to
    fit and returned alone.
    """
    if not chunks:
        return []

    result: list[dict] = []
    token_budget = max_tokens

    for chunk in chunks:
        content = chunk.get("content", "")
        est = _estimate_tokens(content)
        if est <= token_budget:
            result.append(chunk)
            token_budget -= est
        elif not result:
            # Single oversized chunk: truncate to fit.
            words = content.split()
            allowed = int(max_tokens / 1.3)
            truncated = " ".join(words[:allowed])
            result.append({**chunk, "content": truncated})
            break
        else:
            break

    return result
