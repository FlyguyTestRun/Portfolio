#!/usr/bin/env python3
"""Evaluation harness for the Chiller 3 query dataset."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from falcon_grounds.config import MAX_COST_PER_REQUEST_USD
from falcon_grounds.graph.supervisor import run_query

console = Console()
DATASET_PATH = Path(__file__).parent / "datasets" / "chiller_queries.json"


def main() -> None:
    console.print(Rule("[bold blue]falcon-grounds eval[/bold blue]"))

    with open(DATASET_PATH) as f:
        queries = json.load(f)

    results_table = Table(show_header=True, header_style="bold")
    results_table.add_column("ID", style="cyan", width=4)
    results_table.add_column("Query", width=45)
    results_table.add_column("Route", width=14)
    results_table.add_column("Conf.", justify="right", width=6)
    results_table.add_column("Cost USD", justify="right", width=10)
    results_table.add_column("Pass", width=5)

    passed = 0
    total = len(queries)

    for item in queries:
        qid = item["id"]
        query = item["query"]
        console.print(f"Running {qid}: {query[:60]}...")

        try:
            state = run_query(query, tenant_id="meridian")
            route = state.get("route", "error")
            answer = state.get("answer", "")
            confidence = state.get("confidence_score", 0.0)
            cost = state.get("total_cost_usd", 0.0)
            error = state.get("error")

            ok = (
                route != "error"
                and len(answer) > 0
                and confidence >= 0.0
                and cost <= MAX_COST_PER_REQUEST_USD
                and error is None
            )
        except Exception as exc:
            route, answer, confidence, cost, ok = "error", "", 0.0, 0.0, False
            console.print(f"  [red]Exception: {exc}[/red]")

        status = "[green]PASS[/green]" if ok else "[red]FAIL[/red]"
        if ok:
            passed += 1

        results_table.add_row(
            qid,
            query[:45],
            route,
            f"{confidence:.2f}",
            f"${cost:.5f}",
            status,
        )

    console.print()
    console.print(results_table)
    console.print()
    console.print(f"Result: {passed}/{total} passed ({100*passed//total}%)")

    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
