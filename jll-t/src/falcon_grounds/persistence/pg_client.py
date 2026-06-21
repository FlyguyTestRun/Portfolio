"""PostgreSQL client using psycopg v3. Handles schema initialization, CRUD
for all domain tables, and audit logging. Uses DATABASE_URL from config."""

from __future__ import annotations

import json
import warnings
from typing import Any

from falcon_grounds.config import DATABASE_URL, RUNTIME_MODE, RuntimeMode

SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS assets (
    id          TEXT PRIMARY KEY,
    tenant_id   TEXT NOT NULL,
    name        TEXT,
    type        TEXT,
    location    TEXT,
    metadata    JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS work_orders (
    id          TEXT PRIMARY KEY,
    tenant_id   TEXT NOT NULL,
    asset_id    TEXT,
    status      TEXT,
    description TEXT,
    priority    TEXT DEFAULT 'medium',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    metadata    JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS policies (
    id          TEXT PRIMARY KEY,
    tenant_id   TEXT NOT NULL,
    name        TEXT,
    content     TEXT,
    category    TEXT DEFAULT 'general'
);

CREATE TABLE IF NOT EXISTS manuals (
    id          TEXT PRIMARY KEY,
    tenant_id   TEXT NOT NULL,
    asset_type  TEXT,
    title       TEXT,
    content     TEXT
);

CREATE TABLE IF NOT EXISTS audit_log (
    id          SERIAL PRIMARY KEY,
    run_id      TEXT,
    tenant_id   TEXT,
    event_type  TEXT,
    details     JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hitl_decisions (
    id          SERIAL PRIMARY KEY,
    run_id      TEXT,
    decision    TEXT,
    reason      TEXT,
    decided_at  TIMESTAMPTZ DEFAULT NOW()
);
"""


def get_connection() -> Any | None:
    """Return a psycopg v3 connection or None if unavailable."""
    if not DATABASE_URL:
        warnings.warn("DATABASE_URL is not set. PostgreSQL operations are disabled.", stacklevel=2)
        return None
    try:
        import psycopg
        return psycopg.connect(DATABASE_URL)
    except Exception as exc:
        if RUNTIME_MODE == RuntimeMode.LOCAL:
            warnings.warn(f"PostgreSQL not available: {exc}. Run 'make up' to start services.", stacklevel=2)
        else:
            raise
        return None


def _row_to_dict(cursor: Any, row: tuple) -> dict:
    cols = [desc[0] for desc in cursor.description]
    return dict(zip(cols, row))


def init_schema() -> None:
    """Create all tables and extensions. Safe to call multiple times (IF NOT EXISTS)."""
    conn = get_connection()
    if conn is None:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)


def query_asset(asset_id: str, tenant_id: str) -> dict | None:
    conn = get_connection()
    if conn is None:
        return None
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM assets WHERE id = %s AND tenant_id = %s", (asset_id, tenant_id))
            row = cur.fetchone()
            return _row_to_dict(cur, row) if row else None


def query_all_assets(tenant_id: str) -> list[dict]:
    conn = get_connection()
    if conn is None:
        return []
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM assets WHERE tenant_id = %s", (tenant_id,))
            return [_row_to_dict(cur, row) for row in cur.fetchall()]


def query_work_orders(asset_id: str, tenant_id: str) -> list[dict]:
    conn = get_connection()
    if conn is None:
        return []
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM work_orders WHERE asset_id = %s AND tenant_id = %s ORDER BY created_at DESC",
                (asset_id, tenant_id),
            )
            return [_row_to_dict(cur, row) for row in cur.fetchall()]


def query_all_work_orders(tenant_id: str) -> list[dict]:
    conn = get_connection()
    if conn is None:
        return []
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM work_orders WHERE tenant_id = %s ORDER BY created_at DESC", (tenant_id,))
            return [_row_to_dict(cur, row) for row in cur.fetchall()]


def query_policies(tenant_id: str) -> list[dict]:
    conn = get_connection()
    if conn is None:
        return []
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM policies WHERE tenant_id = %s", (tenant_id,))
            return [_row_to_dict(cur, row) for row in cur.fetchall()]


def query_manuals(asset_type: str, tenant_id: str) -> list[dict]:
    conn = get_connection()
    if conn is None:
        return []
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM manuals WHERE asset_type = %s AND tenant_id = %s", (asset_type, tenant_id))
            return [_row_to_dict(cur, row) for row in cur.fetchall()]


def query_all_manuals(tenant_id: str) -> list[dict]:
    conn = get_connection()
    if conn is None:
        return []
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM manuals WHERE tenant_id = %s", (tenant_id,))
            return [_row_to_dict(cur, row) for row in cur.fetchall()]


def insert_asset(asset: dict) -> None:
    conn = get_connection()
    if conn is None:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO assets (id, tenant_id, name, type, location, metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name, type = EXCLUDED.type,
                    location = EXCLUDED.location, metadata = EXCLUDED.metadata
                """,
                (
                    asset["id"], asset["tenant_id"], asset.get("name"), asset.get("type"),
                    asset.get("location"), json.dumps(asset.get("metadata", {})),
                ),
            )


def insert_work_order(wo: dict) -> None:
    conn = get_connection()
    if conn is None:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO work_orders (id, tenant_id, asset_id, status, description, priority, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    status = EXCLUDED.status, description = EXCLUDED.description,
                    priority = EXCLUDED.priority, metadata = EXCLUDED.metadata,
                    updated_at = NOW()
                """,
                (
                    wo["id"], wo["tenant_id"], wo.get("asset_id"), wo.get("status"),
                    wo.get("description"), wo.get("priority", "medium"), json.dumps(wo.get("metadata", {})),
                ),
            )


def insert_policy(policy: dict) -> None:
    conn = get_connection()
    if conn is None:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO policies (id, tenant_id, name, content, category)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name, content = EXCLUDED.content, category = EXCLUDED.category
                """,
                (policy["id"], policy["tenant_id"], policy.get("name"), policy.get("content"), policy.get("category", "general")),
            )


def insert_manual(manual: dict) -> None:
    conn = get_connection()
    if conn is None:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO manuals (id, tenant_id, asset_type, title, content)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    asset_type = EXCLUDED.asset_type, title = EXCLUDED.title, content = EXCLUDED.content
                """,
                (manual["id"], manual["tenant_id"], manual.get("asset_type"), manual.get("title"), manual.get("content")),
            )


def log_audit_event(run_id: str, tenant_id: str, event_type: str, details: dict) -> None:
    conn = get_connection()
    if conn is None:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO audit_log (run_id, tenant_id, event_type, details) VALUES (%s, %s, %s, %s)",
                (run_id, tenant_id, event_type, json.dumps(details)),
            )


def record_hitl_decision(run_id: str, decision: str, reason: str) -> None:
    conn = get_connection()
    if conn is None:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO hitl_decisions (run_id, decision, reason) VALUES (%s, %s, %s)",
                (run_id, decision, reason),
            )
