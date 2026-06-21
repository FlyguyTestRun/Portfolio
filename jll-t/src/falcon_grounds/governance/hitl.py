"""Human-in-the-loop gate. In local mode, prompts via console with a 5-second
auto-approve for demo flow. In cloud mode, posts to a webhook and returns pending."""

from __future__ import annotations

from falcon_grounds.config import HITL_WEBHOOK_URL, RUNTIME_MODE, RuntimeMode
from falcon_grounds.graph.state import AgentState

try:
    from rich.console import Console
    from rich.panel import Panel
    _console = Console()
    _rich_available = True
except ImportError:
    _console = None  # type: ignore[assignment]
    _rich_available = False


def format_hitl_summary(state: AgentState) -> str:
    """Build a structured summary of the proposed action for the reviewer."""
    lines = [
        f"Run ID:           {state.get('run_id', 'unknown')}",
        f"Asset ID:         {state.get('asset_id') or 'not specified'}",
        f"Tenant:           {state.get('tenant_id', 'unknown')}",
        f"Confidence score: {state.get('confidence_score', 0.0):.2f}",
        f"Policy flags:     {', '.join(state.get('policy_flags', [])) or 'none'}",
        "",
        "Proposed action:",
        f"  {state.get('proposed_action', 'none')}",
        "",
        "Compliance evidence:",
    ]
    for item in state.get("compliance_evidence", []):
        lines.append(f"  - {item}")
    return "\n".join(lines)


def request_hitl_approval(state: AgentState) -> str:
    """Request human approval for a proposed action.

    Local mode: prints a Rich panel and waits for keyboard input.
    Auto-approves after 5 seconds for demo flow.

    Cloud mode: posts to HITL_WEBHOOK_URL and returns 'pending'.
    """
    if RUNTIME_MODE == RuntimeMode.LOCAL:
        summary = format_hitl_summary(state)
        if _rich_available and _console:
            _console.print(Panel(summary, title="[bold yellow]HITL Review Required[/bold yellow]", border_style="yellow"))
            _console.print("[yellow]Action required: [a]pprove / [r]eject / [Enter] to auto-approve[/yellow]")
        else:
            print("\n--- HITL REVIEW ---")
            print(summary)
            print("Action required: [a]pprove / [r]eject / [Enter] to auto-approve")

        try:
            choice = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            choice = "a"

        if choice == "r":
            return "rejected"
        return "approved"

    # Cloud/hybrid mode.
    if not HITL_WEBHOOK_URL:
        return "pending"

    try:
        import httpx
        httpx.post(HITL_WEBHOOK_URL, json={"summary": format_hitl_summary(state), "run_id": state.get("run_id")}, timeout=5)
    except Exception:
        pass
    return "pending"
