# ADR 0007: Tool-Context Discipline

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

LangGraph and LangChain support tool-calling agents that receive a tool catalog
in the context. Tool definitions include names, descriptions, and JSON schemas,
typically consuming 50 to 150 tokens per tool. If the full catalog is included on
every call, input tokens scale linearly with catalog size regardless of which tools
the current step actually needs.

A retrieval node does not need work order creation tools. A compliance node does
not need asset search tools. Including these is not just wasteful, it also creates
the risk of a model attempting to call a tool that is not appropriate for the current
step.

## Decision

Layer 6 implements step-specific tool loading via `STEP_TOOL_MAP` in
`src/falcon_grounds/tools/tool_loader.py`. Each step receives only the 2 to 3 tools
it can call. The function `load_tools_for_step(step_name)` returns the tool name
list for the current step. Unknown step names return an empty list.

Current mappings:
- `retrieval`: `search_assets`, `search_work_orders`, `search_manuals`
- `compliance`: `check_policy`, `check_warranty`
- `maintenance`: `create_work_order`, `update_asset_status`
- `supervisor`: `route_to_retrieval`, `route_to_compliance`, `route_to_maintenance`

## Consequences

With a 12-tool catalog and step-specific loading of 3 tools, tool-context discipline
reduces tool-definition tokens by 75 percent per step. Adding new tools to the
catalog does not increase per-step cost because new tools are only added to steps
that need them.

Steps that should not call tools receive an empty list. This also reduces the risk
of the model attempting to call a tool that is not available or appropriate for the
current graph node.

## Alternatives Considered

**Load all tools on every call.** Rejected because with a 12-tool catalog at 100
tokens per definition, this adds 1,200 tokens to every call. At the frontier rate,
that is $0.018 per 1,000 calls in tool-definition overhead alone.

**Dynamic tool loading based on query content.** Rejected for Phase 1 because it
requires another model call or a heuristic that is no better than step-based loading.
The step already encodes what task is being performed, which fully determines which
tools are relevant.
