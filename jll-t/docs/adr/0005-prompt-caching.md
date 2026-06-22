# ADR 0005: Provider-Native Prompt Caching

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

System prompts for facilities analysts, compliance checkers, and work order creators
are stable across requests. Sending these (150 to 500 tokens each) on every API call
incurs full input token charges. Major LLM providers (OpenAI, Anthropic) support
cached prefixes that reduce input token charges by up to 90 percent when the prompt
prefix is identical across calls.

To benefit from provider caching, the cached content must be placed at the start of
the message list and remain unchanged between calls.

## Decision

Layer 4 maintains a `PromptCache` class that builds system prompts once in-process
and returns them from the cache on subsequent calls. The `SYSTEM_PROMPTS` dict
contains three stable prompts: `facilities_analyst`, `compliance_checker`, and
`work_order_creator`.

In cloud mode, the LLM client places the system prompt first in the message list.
The prompt content is never dynamically modified. Per-request context (retrieved
chunks, query text) goes in the user message, not the system prompt.

## Consequences

Up to 90 percent reduction on input token charges for the cached prompt tokens.
A 300-token system prompt charged at $0.0045 on first call costs $0.00045 on
subsequent calls through the provider cache. At 10,000 requests per month, this
saves approximately $40 on the system prompt alone.

In-process caching eliminates prompt build cost after first call. Prompts that
change frequently (personalized, dynamic context) are not placed in the system
prompt and do not receive caching benefit.

## Alternatives Considered

**No caching, build prompt on every call.** Rejected because stable prompts
represent 20 to 40 percent of input tokens on short queries. The optimization
requires no architectural change.

**Disk-based prompt cache.** Unnecessary. In-process memory is sufficient and
faster. The prompts are small (under 500 tokens each) and do not need to persist
across process restarts.

**Dynamic system prompts with request context injected.** Rejected because injecting
per-request data into the system prompt prevents provider-side prefix caching. All
variable content goes in the user message.
