# ADR 0010: Three-Mode Runtime Parity

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

The architecture must be demonstrable locally without any cloud credentials,
testable in a hybrid configuration with Azure OpenAI and local storage, and
deployable to full cloud. If the local mode requires stubs that diverge significantly
from cloud behavior, the demo does not represent the real system and the portfolio
value of the project is reduced.

The specific challenge: external clients (LLM, Redis, Pinecone, Cosmos DB) are
unavailable in local mode. These must degrade gracefully without changing the graph
logic or the calling code.

## Decision

A `RuntimeMode` enum (`LOCAL`, `HYBRID`, `CLOUD`) is read from the `RUNTIME_MODE`
environment variable at startup. All external clients check `RuntimeMode` at
construction time and select the appropriate backend.

`LLMClient` uses `LocalStubClient` in local mode (deterministic responses, no
network calls). `RedisClient` handles `ConnectionError` gracefully and returns
cache misses. `PineconeClient` raises `NotImplementedError` in local mode with a
clear message. `CosmosClient` uses an in-memory dict in local mode.

The graph structure is identical in all three modes. The same node functions,
the same conditional edges, the same state schema. Mode selection affects only
which backend the clients use, not what the graph does.

## Consequences

`make demo` runs the full seven-layer pipeline without any cloud dependencies. The
graph exercises all nodes, writes cost and audit logs, and produces a real answer.
Switching to `HYBRID` mode requires only changing `RUNTIME_MODE` and providing
`AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`. No code changes.

The local demo is a faithful representation of the architecture. The same code paths,
the same state mutations, the same cost accounting. The only difference is the
source of model responses.

## Alternatives Considered

**Maintain a separate demo codebase.** Rejected because divergence between demo and
production code is a known source of misrepresentation in technical interviews. The
goal is to show how the production system works, not a simplified version.

**Hard-code local stubs throughout the graph.** Rejected because it makes mode
switching require code changes rather than configuration changes. Operators could
not switch between modes without a code deployment.

**Require real cloud credentials even for local testing.** Rejected because it
creates a barrier to running the project and generates unnecessary Azure spend
during development.
