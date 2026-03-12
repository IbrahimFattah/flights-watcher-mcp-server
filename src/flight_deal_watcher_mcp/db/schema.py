"""SQL schema definitions for SQLite."""

from __future__ import annotations

SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS user_preferences (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        home_airport TEXT NOT NULL,
        preferred_airlines_json TEXT NOT NULL DEFAULT '[]',
        max_stops INTEGER NOT NULL,
        checked_bag_required INTEGER NOT NULL DEFAULT 0,
        avoid_overnight_layovers INTEGER NOT NULL DEFAULT 0,
        preferred_departure_time_start TEXT NOT NULL,
        preferred_departure_time_end TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS watched_routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_key TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        earliest_departure TEXT NOT NULL,
        latest_departure TEXT NOT NULL,
        return_earliest TEXT,
        return_latest TEXT,
        flex_days INTEGER NOT NULL DEFAULT 0,
        target_price_usd REAL NOT NULL,
        max_stops INTEGER NOT NULL,
        active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS flight_search_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_key TEXT NOT NULL,
        watch_id INTEGER,
        departure_date TEXT NOT NULL,
        return_date TEXT,
        provider TEXT NOT NULL,
        flight_id TEXT NOT NULL,
        price_usd REAL NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (watch_id) REFERENCES watched_routes (id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS deal_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        watch_id INTEGER,
        route_key TEXT NOT NULL,
        flight_id TEXT NOT NULL,
        deal_score REAL,
        reasons_json TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (watch_id) REFERENCES watched_routes (id)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_watched_routes_route_key ON watched_routes(route_key)",
    "CREATE INDEX IF NOT EXISTS idx_flight_search_results_route_key ON flight_search_results(route_key)",
    "CREATE INDEX IF NOT EXISTS idx_deal_alerts_route_key ON deal_alerts(route_key)",
]
