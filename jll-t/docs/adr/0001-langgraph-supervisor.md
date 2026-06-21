# ADR 0001: LangGraph Supervisor Pattern

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

Governed agentic systems for facilities management require typed state propagation
across nodes, support for conditional routing (high confidence vs low confidence vs
compliance hold), and interrupt-resume semantics for human-in-the-loop review of
proposed work orders. The framework choice affects testability, extensibility, and
the ability to inject HITL gates without restructuring the entire graph.

The core requirements are:
- Typed state that prevents silent field omission across node boundaries.
- Conditional routing based on confidence scores and compliance flags.
- The ability to pause execution mid-graph and resume after a human decision.
- Serializable state for durable checkpoint storage.
- Testable node functions that can be exercised independently.

## Decision

Use LangGraph's StateGraph with a TypedDict state schema (AgentState). The
supervisor is a compiled graph, not a prompt-driven agent. Each node is a
deterministic Python function that accepts state and returns updated state.
Conditional edges implement routing logic in plain Python.

The graph entry point is `pre_router`. Conditional edges after `pre_router` and
`compliance` implement the branching logic. The quality guard node has a conditional
edge back to `retrieval` for re-grounding iterations.

## Consequences

Typed state prevents silent field omission across nodes. If a node returns state
missing a required field, the TypedDict check catches it. Compiled graph enables
static analysis of reachable paths. The graph structure is inspectable and testable
without running the full pipeline.

Interrupt-resume enables HITL without polling. The HITL node calls
`request_hitl_approval()`, which in cloud mode posts to a webhook and returns
`pending`. The graph state is persisted to Cosmos DB checkpoints so execution can
resume after the reviewer responds.

State is serializable to Cosmos DB for durable execution across process restarts.

## Alternatives Considered

**AutoGen multi-agent conversation.** Rejected because message-passing semantics
make state reconstruction difficult and cost attribution per-step is not first-class.
Debugging AutoGen graphs requires tracing message history rather than inspecting a
typed state dict.

**Custom async task graph.** Rejected because it duplicates what LangGraph provides
and has no checkpoint support out of the box. Building interrupt-resume semantics
from scratch is non-trivial and error-prone.

**Prompt-driven routing agent.** Rejected because routing decisions that can be
made deterministically should not consume model tokens. A meta-routing model also
introduces non-determinism in a path that should be fully auditable.
