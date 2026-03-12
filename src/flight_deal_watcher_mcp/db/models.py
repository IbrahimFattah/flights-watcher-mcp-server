"""Database-facing record models.

These dataclasses keep repository code easy to read without introducing an ORM.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from flight_deal_watcher_mcp.schemas.tool_inputs import DepartureTimeRange


@dataclass(slots=True)
class TravelPreferencesRecord:
    """Stored user travel preferences."""

    home_airport: str
    preferred_airlines: list[str]
    max_stops: int
    checked_bag_required: bool
    avoid_overnight_layovers: bool
    preferred_departure_time_range: DepartureTimeRange
    created_at: str
    updated_at: str


@dataclass(slots=True)
class WatchedRouteRecord:
    """Stored watched route information."""

    watch_id: int
    route_key: str
    origin: str
    destination: str
    earliest_departure: date
    latest_departure: date
    return_earliest: date | None
    return_latest: date | None
    flex_days: int
    target_price_usd: float
    max_stops: int
    active: bool
    created_at: str
    updated_at: str


@dataclass(slots=True)
class FlightSearchResultRecord:
    """Stored flight search snapshot for future history comparisons."""

    result_id: int
    route_key: str
    watch_id: int | None
    departure_date: date
    return_date: date | None
    provider: str
    flight_id: str
    price_usd: float
    payload_json: str
    created_at: str


@dataclass(slots=True)
class DealAlertRecord:
    """Stored deal alert row for future deal notifications."""

    alert_id: int
    watch_id: int | None
    route_key: str
    flight_id: str
    deal_score: float | None
    reasons_json: str
    payload_json: str
    created_at: str
