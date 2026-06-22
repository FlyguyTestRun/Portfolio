#!/usr/bin/env python3
"""Push eval results to LangSmith. Runs the chiller query suite, scores each
result on routing accuracy, groundedness, and cost, then uploads to the
LangSmith dataset. Works offline when LANGCHAIN_API_KEY is not set."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from falcon_grounds.graph.supervisor import run_query
from falcon_grounds.observability.langsmith_tracer import configure_langsmith, push_eval_result

console = Console()
DATASET_PATH = Path(__file__).parent / "datasets" / "chiller_queries.json"


def main() -> None:
    console.print(Rule("[bold blue]falcon-grounds LangSmith eval[/bold blue]"))

    tracing_active = configure_langsmith()
    if tracing_active:
        console.print("[green]LangSmith tracing active. Results pushed to dataset.[/green]")
    else:
        console.print("[yellow]LANGCHAIN_API_KEY not set. Running offline, results printed only.[/yellow]")

    with open(DATASET_PATH) as f:
        queries = json.load(f)

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="cyan", width=4)
    table.add_column("Query", width=45)
    table.add_column("Route", width=13)
    table.add_column("Grounded", width=8)
    table.add_column("Conf.", justify="right", width=6)
    table.add_column("Cost USD", justify="right", width=10)
    table.add_column("Pushed", width=6)

    for item in queries:
        qid = item["id"]
        query = item["query"]

        try:
            state = run_query(query, tenant_id="meridian")
            route = state.get("route", "error")
            answer = state.get("answer", "")
            confidence = float(state.get("confidence_score", 0.0))
            cost = float(state.get("total_cost_usd", 0.0))
            grounded = bool(state.get("grounded", False))
            run_id = state.get("run_id", qid)

            scores = {
                "route": route,
                "confidence": confidence,
                "grounded": grounded,
                "cost_usd": cost,
            }
            pushed = push_eval_result(run_id=run_id, query=query, answer=answer, scores=scores)
        except Exception as exc:
            route, answer, confidence, cost, grounded, pushed = "error", "", 0.0, 0.0, False, False
            console.print(f"  [red]Exception on {qid}: {exc}[/red]")

        table.add_row(
            qid,
            query[:45],
            route,
            "[green]Y[/green]" if grounded else "[red]N[/red]",
            f"{confidence:.2f}",
            f"${cost:.5f}",
            "[green]Y[/green]" if pushed else "[dim]N[/dim]",
        )

    console.print()
    console.print(table)
    console.print()
    if tracing_active:
        from falcon_grounds.config import LANGCHAIN_PROJECT, LANGSMITH_DATASET_NAME
        console.print(f"Dataset: [bold]{LANGSMITH_DATASET_NAME}[/bold] in project [bold]{LANGCHAIN_PROJECT}[/bold]")


if __name__ == "__main__":
    main()
