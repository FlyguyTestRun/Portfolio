"""Lightweight span tracing using contextvars. In cloud mode, spans would be
forwarded to LangSmith or an OTel collector."""

from __future__ import annotations

import time
from contextvars import ContextVar
from dataclasses import dataclass, field


@dataclass
class Span:
    run_id: str
    step: str
    start_time: float = field(default_factory=time.monotonic)


_current_span: ContextVar[Span | None] = ContextVar("_current_span", default=None)


def start_span(step: str, run_id: str = "") -> Span:
    """Create and register a new span for the given step."""
    span = Span(run_id=run_id, step=step)
    _current_span.set(span)
    return span


def end_span(span: Span) -> dict:
    """Close a span and return its timing metadata."""
    duration_ms = (time.monotonic() - span.start_time) * 1000
    return {"run_id": span.run_id, "step": span.step, "duration_ms": round(duration_ms, 2)}


def get_current_span() -> Span | None:
    """Return the currently active span, or None if outside a span context."""
    return _current_span.get()
