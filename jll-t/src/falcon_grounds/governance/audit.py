"""Append-only audit log. Every graph event is written to a JSONL file.
In cloud mode, events are also persisted to the PostgreSQL audit_log table."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

AUDIT_LOG = Path("logs/audit.jsonl")


def log_event(run_id: str, tenant_id: str, event_type: str, details: dict) -> None:
    """Append an audit event to the JSONL log file."""
    try:
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "run_id": run_id,
            "tenant_id": tenant_id,
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with AUDIT_LOG.open("a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass
