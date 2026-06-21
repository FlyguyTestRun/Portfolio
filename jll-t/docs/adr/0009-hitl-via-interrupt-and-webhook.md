# ADR 0009: HITL via Graph Interrupt and Webhook

**Status:** Accepted
**Date:** 2026-06-20
**Deciders:** Bryan Shaw

## Context

Facilities management work orders carry operational and financial consequences.
Automated work order creation without human review creates risk of incorrect scope,
warranty violations, or safety issues. The system must support pausing execution for
approval without losing graph state, without blocking the caller indefinitely, and
without requiring a polling loop that holds compute.

Two interaction modes are required: synchronous (local demo, fast review) and
asynchronous (production, reviewer notified via webhook and responds when available).

## Decision

The HITL gate is implemented as a graph node (`node_hitl` in `supervisor.py`).
The `request_hitl_approval()` function in `governance/hitl.py` has two behaviors:

Local mode: prints a Rich panel with the proposed action summary and waits for
console input. Auto-approves after user presses Enter or after an EOFError (for
non-interactive demo runs). Returns `approved` or `rejected` synchronously.

Cloud/hybrid mode: posts the action summary to `HITL_WEBHOOK_URL`. Returns `pending`.
The `/webhooks/approve/{run_id}` and `/webhooks/reject/{run_id}` endpoints record
the decision via the audit log and `pg_client.record_hitl_decision()`.

The HITL decision is recorded in state as `hitl_decision`. The audit log captures
the decision with timestamp and run_id.

## Consequences

Human approval is mandatory for any action flagged by the compliance agent (policy
flags raised or confidence below `CONFIDENCE_HITL_THRESHOLD`). The graph state
survives the pause in cloud mode via Cosmos DB checkpoints. Reviewers receive a
structured summary, not raw model output.

Local mode enables full demo flow without webhook infrastructure. The same code path
runs in both modes, so the demo is representative of production behavior.

## Alternatives Considered

**Poll for approval with a sleeping loop.** Rejected because it holds compute and
cannot survive process restart. A sleeping loop also fails if the reviewer takes
longer than the polling timeout.

**Require synchronous approval within the request cycle.** Rejected because reviewer
latency is unpredictable. A 30-second timeout would fail for reviewers who are away
from their desk, and a longer timeout would block the API caller.

**Skip HITL for all actions.** Rejected because unreviewed work orders on warranted
equipment create warranty and compliance risk. HITL is a governance requirement, not
an optional feature.
