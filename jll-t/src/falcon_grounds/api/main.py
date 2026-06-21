"""FastAPI application entry point. Initializes the database schema on startup
and exposes query, cost reporting, and health endpoints."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from pydantic import BaseModel

from falcon_grounds.api.webhooks import router as webhooks_router
from falcon_grounds.config import RUNTIME_MODE
from falcon_grounds.graph.supervisor import run_query
from falcon_grounds.observability.cost_attribution import generate_report
from falcon_grounds.observability.langsmith_tracer import configure_langsmith
from falcon_grounds.persistence import pg_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    pg_client.init_schema()
    configure_langsmith()
    yield


app = FastAPI(
    title="Falcon Grounds API",
    description="Governed agentic facilities-management AI reference architecture.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(webhooks_router)


class QueryRequest(BaseModel):
    query: str
    tenant_id: str = "meridian"
    asset_id: str | None = None


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "mode": RUNTIME_MODE.value, "version": "0.1.0"}


@app.post("/query")
async def query_endpoint(request: QueryRequest) -> dict:
    """Run the agent graph and return the final state as JSON."""
    state = run_query(request.query, tenant_id=request.tenant_id, asset_id=request.asset_id)
    return dict(state)


@app.get("/cost-report")
async def cost_report() -> dict:
    """Return the aggregated cost report from the JSONL log."""
    report = generate_report()
    return report.__dict__
