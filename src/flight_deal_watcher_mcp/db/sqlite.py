"""SQLite connection helpers."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flight_deal_watcher_mcp.db.schema import SCHEMA_STATEMENTS


def create_connection(database_path: Path) -> sqlite3.Connection:
    """Create a SQLite connection configured for repository use."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    """Create the SQLite schema if it does not exist yet."""
    with connection:
        for statement in SCHEMA_STATEMENTS:
            connection.execute(statement)
