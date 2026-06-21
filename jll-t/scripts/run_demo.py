#!/usr/bin/env python3
"""
Demo runner for the Chiller 3 high head pressure scenario. Runs the full
agent graph in local mode and prints a formatted trace to the console.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

from falcon_grounds.graph.supervisor import run_query

console = Console()

DEMO_QUERY = (
    "Chiller 3 in Tower A is reporting intermittent high head pressure. "
    "What is the history, what is the likely cause, is there a warranty or "
    "compliance constraint, and what work order should we open?"
)
DEMO_ASSET_ID = "ASSET-CHI-3A"
DEMO_TENANT = "meridian"


def main() -> None:
    console.print(Rule("[bold blue]falcon-grounds demo[/bold blue]"))
    console.print()
    console.print(Panel(DEMO_QUERY, title="Query", border_style="blue"))
    console.print()
    console.print("[bold]Running agent graph...[/bold]")

    t0 = time.monotonic()
    state = run_query(DEMO_QUERY, tenant_id=DEMO_TENANT, asset_id=DEMO_ASSET_ID)
    elapsed = time.monotonic() - t0

    console.print()
    console.print(Rule("[bold]Trace Summary[/bold]"))

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Layer / Step", style="cyan", min_width=30)
    table.add_column("Result")

    route_rationale = state.get("routing_rationale", "")[:80]
    table.add_row("Layer 1: Pre-router", f"Route: [bold]{state.get('route', '?')}[/bold]  |  {route_rationale}")
    table.add_row("Layer 2: Cache", "Miss (local mode, no external embedding model)")
    table.add_row("Layer 3: Model tier", state.get("model_tier", "none"))

    chunks = state.get("retrieval_chunks", [])
    sources = ", ".join(state.get("retrieval_sources", [])) or "none"
    table.add_row("Retrieval agent", f"{len(chunks)} chunk(s) from: {sources}")

    score = state.get("confidence_score", 0.0)
    hitl_req = state.get("requires_hitl", False)
    table.add_row("Compliance / confidence", f"Score: {score:.2f}  |  HITL required: {hitl_req}")

    action = state.get("proposed_action", "")
    table.add_row("Maintenance agent", (action[:80] + "...") if len(action) > 80 else action)
    table.add_row("Quality guard", f"Grounded: {state.get('grounded', False)}")
    table.add_row("Work order ID", state.get("work_order_id") or "N/A")
    table.add_row("Total cost", f"${state.get('total_cost_usd', 0.0):.5f}")
    table.add_row("Elapsed", f"{elapsed:.2f}s")

    console.print(table)
    console.print()

    answer = state.get("answer", "No answer generated.")
    console.print(Panel(answer, title="[bold green]Answer[/bold green]", border_style="green"))

    layers = state.get("cost_layers", {})
    if layers:
        console.print()
        cost_table = Table(title="Cost by Layer", show_header=True, header_style="bold magenta")
        cost_table.add_column("Layer")
        cost_table.add_column("Cost (USD)", justify="right")
        for layer, cost in layers.items():
            cost_table.add_row(layer, f"${cost:.5f}")
        cost_table.add_row("[bold]TOTAL[/bold]", f"[bold]${state.get('total_cost_usd', 0.0):.5f}[/bold]")
        console.print(cost_table)

    console.print()
    console.print("[dim]Run 'make costreport' to see the aggregated cost report.[/dim]")


if __name__ == "__main__":
    main()
