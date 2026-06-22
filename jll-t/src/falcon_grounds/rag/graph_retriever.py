"""Graph RAG retriever for facilities entity relationships.

Builds an in-memory networkx DiGraph from seed data: assets linked to work
orders, policies, and manuals. After standard vector retrieval, enrich()
traverses the graph to append multi-hop context that keyword and vector
search would miss (e.g., all work orders for an asset mentioned in a manual).

GRAPH_RETRIEVAL_ENABLED=false by default. Enable for demos requiring
multi-hop reasoning across assets, work orders, and policies.

In CLOUD mode with GRAPH_BACKEND=neo4j, delegates to Neo4jGraph from
langchain-community. The networkx path has zero external dependencies.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

import networkx as nx

import falcon_grounds.config as cfg
from falcon_grounds.config import RuntimeMode

_SEED_DIR = Path(__file__).parent.parent.parent.parent / "seed"
_ASSET_ID_RE = re.compile(r"ASSET-[A-Z0-9\-]+")
_WO_ID_RE = re.compile(r"WO-\d{4}-\d{4}")


def _load_seed(filename: str) -> list[dict]:
    path = _SEED_DIR / filename
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []


class FacilitiesGraphRetriever:
    """Networkx entity graph for local and hybrid modes, Neo4j for cloud."""

    def __init__(self) -> None:
        self._graph: Optional[nx.DiGraph] = None
        if cfg.GRAPH_BACKEND != "neo4j" or cfg.RUNTIME_MODE != RuntimeMode.CLOUD:
            self._graph = self._build_local_graph()

    def _build_local_graph(self) -> nx.DiGraph:
        g: nx.DiGraph = nx.DiGraph()
        assets = _load_seed("assets.json")
        work_orders = _load_seed("work_orders.json")
        policies = _load_seed("policies.json")
        manuals = _load_seed("manuals.json")

        for a in assets:
            g.add_node(a["id"], type="asset", name=a.get("name", ""), asset_type=a.get("type", ""), data=a)

        for wo in work_orders:
            g.add_node(
                wo["id"],
                type="work_order",
                status=wo.get("status", ""),
                priority=wo.get("priority", ""),
                data=wo,
            )
            asset_id = wo.get("asset_id")
            if asset_id and asset_id in g:
                g.add_edge(asset_id, wo["id"], rel="has_work_order")
                g.add_edge(wo["id"], asset_id, rel="for_asset")

        for pol in policies:
            g.add_node(
                pol["id"],
                type="policy",
                name=pol.get("name", ""),
                category=pol.get("category", ""),
                data=pol,
            )

        for man in manuals:
            g.add_node(
                man["id"],
                type="manual",
                title=man.get("title", ""),
                asset_type=man.get("asset_type", ""),
                data=man,
            )

        for a in assets:
            asset_type = a.get("type", "")
            for man in manuals:
                if man.get("asset_type") == asset_type:
                    g.add_edge(a["id"], man["id"], rel="has_manual")
            for pol in policies:
                if pol.get("category") in ("warranty", "operations"):
                    g.add_edge(a["id"], pol["id"], rel="governed_by")

        return g

    def enrich(self, chunks: list[dict], depth: int = 2) -> list[dict]:
        """Append graph-neighbor context chunks. Returns original list if graph unavailable."""
        if not chunks or self._graph is None:
            return chunks

        found_ids: set[str] = set()
        for chunk in chunks:
            text = chunk.get("content", "") + " " + chunk.get("id", "")
            found_ids.update(_ASSET_ID_RE.findall(text))
            found_ids.update(_WO_ID_RE.findall(text))

        enriched = list(chunks)
        seen_ids: set[str] = {c.get("id", "") for c in chunks}

        for entity_id in found_ids:
            if entity_id not in self._graph:
                continue
            neighbors: set[str] = set()
            frontier = {entity_id}
            for _ in range(depth):
                next_frontier: set[str] = set()
                for node in frontier:
                    next_frontier.update(self._graph.successors(node))
                neighbors.update(next_frontier)
                frontier = next_frontier

            for neighbor_id in neighbors:
                if neighbor_id in seen_ids:
                    continue
                node_data = self._graph.nodes[neighbor_id]
                raw: dict = node_data.get("data", {})
                summary = raw.get("content") or raw.get("description") or raw.get("name", "")
                if not summary:
                    continue
                enriched.append({
                    "id": neighbor_id,
                    "content": f"[Graph context: {node_data.get('type', 'entity')}] {summary}",
                    "source": f"graph:{node_data.get('type', 'entity')}",
                    "score": 0.5,
                    "store": "graph",
                })
                seen_ids.add(neighbor_id)

        return enriched
