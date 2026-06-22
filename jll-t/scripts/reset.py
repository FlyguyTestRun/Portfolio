#!/usr/bin/env python3
"""Drop and recreate all database tables. Delete local logs."""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console

from falcon_grounds.persistence import pg_client

console = Console()

DROP_SQL = """
DROP TABLE IF EXISTS hitl_decisions CASCADE;
DROP TABLE IF EXISTS audit_log CASCADE;
DROP TABLE IF EXISTS manuals CASCADE;
DROP TABLE IF EXISTS policies CASCADE;
DROP TABLE IF EXISTS work_orders CASCADE;
DROP TABLE IF EXISTS assets CASCADE;
"""


def main() -> None:
    console.print("[bold red]falcon-grounds reset[/bold red]")
    console.print("Dropping tables...")
    conn = pg_client.get_connection()
    if conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(DROP_SQL)
        console.print("  Tables dropped.")

    console.print("Recreating schema...")
    pg_client.init_schema()
    console.print("  Schema recreated.")

    logs_dir = Path("logs")
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
        console.print("  Logs directory deleted.")

    console.print("[green]Reset complete. Run 'make seed' to reload fixture data.[/green]")


if __name__ == "__main__":
    main()
