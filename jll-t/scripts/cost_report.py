#!/usr/bin/env python3
"""Print the aggregated cost report from the JSONL cost log."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from falcon_grounds.observability.cost_attribution import LOG_FILE, generate_report

console = Console()

LAYER_DESCRIPTIONS = {
    "retrieval": "PostgreSQL keyword/vector search",
    "compliance": "LLM confidence and policy assessment",
    "maintenance": "Work order proposal generation",
    "supervisor": "Model tier selection (routing call)",
}


def main() -> None:
    if not LOG_FILE.exists():
        console.print("[yellow]No requests logged yet. Run 'make demo' first.[/yellow]")
        return

    report = generate_report()

    console.print(Rule("[bold blue]falcon-grounds cost report[/bold blue]"))
    console.print()

    summary = Table(title="Summary", show_header=True, header_style="bold")
    summary.add_column("Metric")
    summary.add_column("Value", justify="right")
    summary.add_row("Total requests", str(report.total_requests))
    summary.add_row("Total cost (USD)", f"${report.total_cost_usd:.5f}")
    summary.add_row("Total savings vs baseline (USD)", f"${report.total_savings_usd:.5f}")
    summary.add_row("Cache hits", str(report.cache_hits))
    summary.add_row("Pre-route hits (zero model cost)", str(report.preroute_hits))
    console.print(summary)
    console.print()

    layer_table = Table(title="Cost by Layer", show_header=True, header_style="bold cyan")
    layer_table.add_column("Layer")
    layer_table.add_column("Total Cost (USD)", justify="right")
    layer_table.add_column("Description")
    for layer, cost in sorted(report.by_layer.items(), key=lambda x: x[1], reverse=True):
        desc = LAYER_DESCRIPTIONS.get(layer, "")
        layer_table.add_row(layer, f"${cost:.5f}", desc)
    console.print(layer_table)
    console.print()

    tier_table = Table(title="Requests by Model Tier", show_header=True, header_style="bold magenta")
    tier_table.add_column("Tier")
    tier_table.add_column("Count", justify="right")
    for tier, count in sorted(report.by_tier.items()):
        tier_table.add_row(tier, str(count))
    console.print(tier_table)


if __name__ == "__main__":
    main()
