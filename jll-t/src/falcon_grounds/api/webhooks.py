"""HITL webhook endpoints. Reviewers call /webhooks/approve/{run_id} or
/webhooks/reject/{run_id} to resume a paused graph execution."""

from __future__ import annotations

from fastapi import APIRouter

from falcon_grounds.governance.audit import log_event
from falcon_grounds.persistence import pg_client

router = APIRouter(prefix="/webhooks", tags=["hitl"])


@router.post("/approve/{run_id}")
async def approve(run_id: str) -> dict:
    """Record an approval decision for the given run."""
    log_event(run_id, "system", "hitl_decision", {"decision": "approved"})
    pg_client.record_hitl_decision(run_id, "approved", "Approved via webhook.")
    return {"status": "approved", "run_id": run_id}


@router.post("/reject/{run_id}")
async def reject(run_id: str) -> dict:
    """Record a rejection decision for the given run."""
    log_event(run_id, "system", "hitl_decision", {"decision": "rejected"})
    pg_client.record_hitl_decision(run_id, "rejected", "Rejected via webhook.")
    return {"status": "rejected", "run_id": run_id}
