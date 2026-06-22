"""LangSmith tracing configuration and eval dataset integration.

LangGraph auto-instruments every node when LANGCHAIN_TRACING_V2=true and
LANGCHAIN_API_KEY is set. This module handles startup configuration and
provides push_eval_result() for the eval harness to record scored runs.
"""

from __future__ import annotations

import os
from typing import Any

import falcon_grounds.config as cfg


def configure_langsmith() -> bool:
    """Set LangSmith env vars from config. Returns True if tracing is active."""
    if not cfg.LANGCHAIN_API_KEY:
        return False
    os.environ["LANGCHAIN_API_KEY"] = cfg.LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = cfg.LANGCHAIN_PROJECT
    os.environ["LANGCHAIN_ENDPOINT"] = cfg.LANGCHAIN_ENDPOINT
    os.environ["LANGCHAIN_TRACING_V2"] = "true" if cfg.LANGCHAIN_TRACING_V2 else "false"
    return cfg.LANGCHAIN_TRACING_V2


def push_eval_result(
    run_id: str,
    query: str,
    answer: str,
    scores: dict[str, Any],
) -> bool:
    """Push one eval result to the LangSmith dataset. Returns False if disabled."""
    if not cfg.LANGCHAIN_API_KEY:
        return False
    try:
        from langsmith import Client  # type: ignore[import-untyped]

        client = Client(api_key=cfg.LANGCHAIN_API_KEY, api_url=cfg.LANGCHAIN_ENDPOINT)
        dataset_name = cfg.LANGSMITH_DATASET_NAME
        existing = {d.name for d in client.list_datasets()}
        if dataset_name not in existing:
            dataset = client.create_dataset(
                dataset_name,
                description="Chiller RAG evaluation suite for falcon-grounds",
            )
        else:
            dataset = next(d for d in client.list_datasets() if d.name == dataset_name)

        client.create_examples(
            inputs=[{"query": query}],
            outputs=[{"answer": answer}],
            metadata=[{"run_id": run_id, **scores}],
            dataset_id=dataset.id,
        )
        return True
    except Exception:
        return False
