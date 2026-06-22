"""
Layer 7 of the cost-control framework. Per-request cost tracking, attribution, and
reporting. Every request writes a structured cost entry to a JSONL log. The cost
report aggregates across requests, shows savings vs a full-frontier baseline, and
can serve as a CI gate on mean cost per request.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from falcon_grounds.graph.state import AgentState

LOG_FILE = Path("logs/cost_log.jsonl")
FRONTIER_BASELINE_PER_REQUEST: float = 0.030  # Estimated full-frontier cost with no optimization.


@dataclass
class CostEntry:
    run_id: str
    tenant_id: str
    query_preview: str
    timestamp: str
    layers: dict[str, float]
    total_cost_usd: float
    route: str
    cache_hit: bool
    model_tier: str
    savings_usd: float


@dataclass
class CostReport:
    total_requests: int
    total_cost_usd: float
    total_savings_usd: float
    cache_hits: int
    preroute_hits: int
    by_tier: dict[str, int] = field(default_factory=dict)
    by_layer: dict[str, float] = field(default_factory=dict)


def record_cost_entry(state: AgentState) -> None:
    """Write a CostEntry for the completed request to the JSONL cost log."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    savings = FRONTIER_BASELINE_PER_REQUEST - state.get("total_cost_usd", 0.0)
    entry = CostEntry(
        run_id=state.get("run_id", ""),
        tenant_id=state.get("tenant_id", ""),
        query_preview=state.get("query", "")[:80],
        timestamp=datetime.now(timezone.utc).isoformat(),
        layers=state.get("cost_layers", {}),
        total_cost_usd=state.get("total_cost_usd", 0.0),
        route=state.get("route", ""),
        cache_hit=state.get("route") == "cached",
        model_tier=state.get("model_tier", "none"),
        savings_usd=max(savings, 0.0),
    )
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(entry.__dict__) + "\n")


def load_cost_log() -> list[CostEntry]:
    """Load all cost entries from the JSONL log file."""
    if not LOG_FILE.exists():
        return []
    entries: list[CostEntry] = []
    with LOG_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                entries.append(CostEntry(**data))
            except Exception:
                continue
    return entries


def generate_report() -> CostReport:
    """Aggregate all cost entries into a summary report."""
    entries = load_cost_log()
    if not entries:
        return CostReport(
            total_requests=0,
            total_cost_usd=0.0,
            total_savings_usd=0.0,
            cache_hits=0,
            preroute_hits=0,
        )

    total_cost = sum(e.total_cost_usd for e in entries)
    total_savings = sum(e.savings_usd for e in entries)
    cache_hits = sum(1 for e in entries if e.cache_hit)
    preroute_hits = sum(1 for e in entries if e.route == "deterministic")

    by_tier: dict[str, int] = {}
    by_layer: dict[str, float] = {}
    for e in entries:
        by_tier[e.model_tier] = by_tier.get(e.model_tier, 0) + 1
        for layer, cost in e.layers.items():
            by_layer[layer] = by_layer.get(layer, 0.0) + cost

    return CostReport(
        total_requests=len(entries),
        total_cost_usd=total_cost,
        total_savings_usd=total_savings,
        cache_hits=cache_hits,
        preroute_hits=preroute_hits,
        by_tier=by_tier,
        by_layer=by_layer,
    )
