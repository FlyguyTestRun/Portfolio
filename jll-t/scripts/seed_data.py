#!/usr/bin/env python3
"""Seed the local PostgreSQL database with Meridian Portfolio fixture data."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console

from falcon_grounds.persistence import pg_client

console = Console()
SEED_DIR = Path(__file__).parent.parent / "seed"


def load_json(filename: str) -> list[dict]:
    path = SEED_DIR / filename
    with open(path) as f:
        return json.load(f)


def main() -> None:
    console.print("[bold blue]falcon-grounds seed[/bold blue]")
    console.print("Initializing schema...")
    try:
        pg_client.init_schema()
    except Exception as exc:
        console.print(f"[red]Schema init failed: {exc}[/red]")
        console.print("[yellow]Is 'docker compose up' running? Try: make up[/yellow]")
        sys.exit(1)

    assets = load_json("assets.json")
    work_orders = load_json("work_orders.json")
    policies = load_json("policies.json")
    manuals = load_json("manuals.json")

    for asset in assets:
        pg_client.insert_asset(asset)
    console.print(f"  Inserted {len(assets)} assets.")

    for wo in work_orders:
        pg_client.insert_work_order(wo)
    console.print(f"  Inserted {len(work_orders)} work orders.")

    for policy in policies:
        pg_client.insert_policy(policy)
    console.print(f"  Inserted {len(policies)} policies.")

    for manual in manuals:
        pg_client.insert_manual(manual)
    console.print(f"  Inserted {len(manuals)} manuals.")

    console.print("[green]Seed complete.[/green]")


if __name__ == "__main__":
    main()
