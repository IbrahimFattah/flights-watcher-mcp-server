"""Repository classes that isolate SQL from the rest of the project."""

from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime, timezone
from typing import Any

from flight_deal_watcher_mcp.db.models import (
    DealAlertRecord,
    FlightSearchResultRecord,
    TravelPreferencesRecord,
    WatchedRouteRecord,
)
from flight_deal_watcher_mcp.schemas.tool_inputs import DepartureTimeRange, SetTravelPreferencesInput, WatchRouteInput
from flight_deal_watcher_mcp.utils.route_keys import build_route_key


def utc_now_iso() -> str:
    """Return a UTC timestamp suitable for persistence."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class UserPreferencesRepository:
    """Repository for the single stored preferences record."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def get(self) -> TravelPreferencesRecord | None:
        """Return the stored preferences record, if one exists."""
        row = self.connection.execute("SELECT * FROM user_preferences WHERE id = 1").fetchone()
        if row is None:
            return None
        return TravelPreferencesRecord(
            home_airport=row["home_airport"],
            preferred_airlines=json.loads(row["preferred_airlines_json"]),
            max_stops=row["max_stops"],
            checked_bag_required=bool(row["checked_bag_required"]),
            avoid_overnight_layovers=bool(row["avoid_overnight_layovers"]),
            preferred_departure_time_range=DepartureTimeRange(
                start=row["preferred_departure_time_start"],
                end=row["preferred_departure_time_end"],
            ),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def upsert(self, preferences: SetTravelPreferencesInput) -> TravelPreferencesRecord:
        """Create or update the single stored preferences record."""
        existing = self.get()
        now = utc_now_iso()
        created_at = existing.created_at if existing is not None else now
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO user_preferences (
                    id,
                    home_airport,
                    preferred_airlines_json,
                    max_stops,
                    checked_bag_required,
                    avoid_overnight_layovers,
                    preferred_departure_time_start,
                    preferred_departure_time_end,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    home_airport = excluded.home_airport,
                    preferred_airlines_json = excluded.preferred_airlines_json,
                    max_stops = excluded.max_stops,
                    checked_bag_required = excluded.checked_bag_required,
                    avoid_overnight_layovers = excluded.avoid_overnight_layovers,
                    preferred_departure_time_start = excluded.preferred_departure_time_start,
                    preferred_departure_time_end = excluded.preferred_departure_time_end,
                    updated_at = excluded.updated_at
                """,
                (
                    1,
                    preferences.home_airport,
                    json.dumps(preferences.preferred_airlines),
                    preferences.max_stops,
                    int(preferences.checked_bag_required),
                    int(preferences.avoid_overnight_layovers),
                    preferences.preferred_departure_time_range.start,
                    preferences.preferred_departure_time_range.end,
                    created_at,
                    now,
                ),
            )
        stored = self.get()
        if stored is None:
            raise RuntimeError("Failed to save travel preferences.")
        return stored


class WatchedRoutesRepository:
    """Repository for watched routes."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(self, watch_input: WatchRouteInput) -> WatchedRouteRecord:
        """Insert a watched route and return the stored record."""
        route_key = build_route_key(
            watch_input.origin,
            watch_input.destination,
            watch_input.return_earliest is not None,
        )
        now = utc_now_iso()
        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO watched_routes (
                    route_key,
                    origin,
                    destination,
                    earliest_departure,
                    latest_departure,
                    return_earliest,
                    return_latest,
                    flex_days,
                    target_price_usd,
                    max_stops,
                    active,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    route_key,
                    watch_input.origin,
                    watch_input.destination,
                    watch_input.earliest_departure.isoformat(),
                    watch_input.latest_departure.isoformat(),
                    watch_input.return_earliest.isoformat() if watch_input.return_earliest else None,
                    watch_input.return_latest.isoformat() if watch_input.return_latest else None,
                    watch_input.flex_days,
                    watch_input.target_price_usd,
                    watch_input.max_stops,
                    1,
                    now,
                    now,
                ),
            )
        row = self.connection.execute(
            "SELECT * FROM watched_routes WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
        if row is None:
            raise RuntimeError("Failed to save watched route.")
        return self._row_to_record(row)

    def list_active(self) -> list[WatchedRouteRecord]:
        """Return all active watched routes ordered by creation time."""
        rows = self.connection.execute(
            "SELECT * FROM watched_routes WHERE active = 1 ORDER BY created_at ASC"
        ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def _row_to_record(self, row: sqlite3.Row) -> WatchedRouteRecord:
        """Convert a SQLite row into a typed record."""
        return WatchedRouteRecord(
            watch_id=row["id"],
            route_key=row["route_key"],
            origin=row["origin"],
            destination=row["destination"],
            earliest_departure=date.fromisoformat(row["earliest_departure"]),
            latest_departure=date.fromisoformat(row["latest_departure"]),
            return_earliest=date.fromisoformat(row["return_earliest"]) if row["return_earliest"] else None,
            return_latest=date.fromisoformat(row["return_latest"]) if row["return_latest"] else None,
            flex_days=row["flex_days"],
            target_price_usd=row["target_price_usd"],
            max_stops=row["max_stops"],
            active=bool(row["active"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )


class FlightSearchResultsRepository:
    """Repository scaffold for storing normalized search snapshots later."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def save(
        self,
        *,
        route_key: str,
        watch_id: int | None,
        departure_date: date,
        return_date: date | None,
        provider: str,
        flight_id: str,
        price_usd: float,
        payload: dict[str, Any],
    ) -> FlightSearchResultRecord:
        """Persist one search result snapshot for future historical comparisons."""
        now = utc_now_iso()
        payload_json = json.dumps(payload)
        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO flight_search_results (
                    route_key,
                    watch_id,
                    departure_date,
                    return_date,
                    provider,
                    flight_id,
                    price_usd,
                    payload_json,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    route_key,
                    watch_id,
                    departure_date.isoformat(),
                    return_date.isoformat() if return_date else None,
                    provider,
                    flight_id,
                    price_usd,
                    payload_json,
                    now,
                ),
            )
        return FlightSearchResultRecord(
            result_id=cursor.lastrowid,
            route_key=route_key,
            watch_id=watch_id,
            departure_date=departure_date,
            return_date=return_date,
            provider=provider,
            flight_id=flight_id,
            price_usd=price_usd,
            payload_json=payload_json,
            created_at=now,
        )


class DealAlertsRepository:
    """Repository scaffold for future deal alerts."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def save(
        self,
        *,
        watch_id: int | None,
        route_key: str,
        flight_id: str,
        deal_score: float | None,
        reasons: list[str],
        payload: dict[str, Any],
    ) -> DealAlertRecord:
        """Persist a deal alert row for future resource exposure."""
        now = utc_now_iso()
        reasons_json = json.dumps(reasons)
        payload_json = json.dumps(payload)
        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO deal_alerts (
                    watch_id,
                    route_key,
                    flight_id,
                    deal_score,
                    reasons_json,
                    payload_json,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    watch_id,
                    route_key,
                    flight_id,
                    deal_score,
                    reasons_json,
                    payload_json,
                    now,
                ),
            )
        return DealAlertRecord(
            alert_id=cursor.lastrowid,
            watch_id=watch_id,
            route_key=route_key,
            flight_id=flight_id,
            deal_score=deal_score,
            reasons_json=reasons_json,
            payload_json=payload_json,
            created_at=now,
        )
