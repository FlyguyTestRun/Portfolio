# ADR 0006: Context Compression

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

Retrieval can surface more content than necessary. A query about chiller head
pressure might retrieve 5,000 tokens of manual text, work order history, and policy
content. Sending all of it to the model increases input token cost proportionally
to the number of chunks retrieved, even when the additional content adds diminishing
value beyond the top 2 to 3 chunks.

## Decision

Layer 5 applies greedy top-k context compression before each model call.
`compress_context()` in `src/falcon_grounds/rag/compress.py` accumulates chunks
in rank order (most relevant first) until the token budget is reached. Token count
is estimated as `word_count * 1.3`, accounting for subword tokenization.

The default budget is 2,000 tokens. A single chunk that exceeds the budget is
truncated to fit and returned alone. An empty chunk list returns an empty list.

Context compression is applied after reranking so the highest-scored chunks are
always included within the budget.

## Consequences

Input tokens are reduced by 30 to 60 percent on document-heavy queries. On a query
that retrieves 5,000 tokens of content, compression to 2,000 tokens saves 0.045
at the frontier rate. Applied to all retrieval-heavy queries, this is a meaningful
reduction.

The quality tradeoff is acceptable: the reranker has already placed the most
relevant chunks first. Truncated chunks are the lower-ranked ones that contribute
least to the answer.

## Alternatives Considered

**Extractive summarization per chunk before passing to the model.** Rejected for
Phase 1 because it adds a model call to reduce a model call. The break-even point
requires the chunk summarization to cost less than the token savings at the main
model. This is viable at high input volumes where chunk content is very long.

**Full chunk inclusion without budget.** Rejected because it inflates context on
every call regardless of relevance. There is no upper bound on how much content
retrieval might surface, and context window limits are finite.

**Fixed top-k without token counting.** Rejected because chunks vary in length.
A fixed top-3 might be 500 tokens or 5,000 tokens depending on the content.
Token-based budgeting is more precise.
