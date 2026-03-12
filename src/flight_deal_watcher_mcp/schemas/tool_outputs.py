"""Output schemas for Phase 1 MCP tools."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from flight_deal_watcher_mcp.schemas.tool_inputs import CabinClass, DepartureTimeRange


class FlightSegmentOutput(BaseModel):
    """One flight segment in a normalized itinerary."""

    origin: str
    destination: str
    departure_at: str
    arrival_at: str
    airline: str
    flight_number: str
    duration_minutes: int
    stops: int = 0


class NormalizedFlightResult(BaseModel):
    """A normalized flight search result returned to the MCP client."""

    flight_id: str
    route_key: str
    provider: str
    cabin: CabinClass
    adults: int
    price_usd: float
    currency: str = "USD"
    checked_bag_included: bool
    is_round_trip: bool
    total_stops: int
    total_duration_minutes: int
    outbound: list[FlightSegmentOutput]
    inbound: list[FlightSegmentOutput] | None = None
    summary: str


class SearchFlightsOutput(BaseModel):
    """Response payload for search_flights."""

    origin: str
    destination: str
    departure_date: date
    return_date: date | None = None
    result_count: int
    results: list[NormalizedFlightResult]
    summary: str


class WatchedRouteOutput(BaseModel):
    """A saved watched route."""

    watch_id: int
    route_key: str
    origin: str
    destination: str
    earliest_departure: date
    latest_departure: date
    return_earliest: date | None = None
    return_latest: date | None = None
    flex_days: int
    target_price_usd: float
    max_stops: int
    active: bool
    created_at: str
    updated_at: str
    summary: str


class ListWatchedRoutesOutput(BaseModel):
    """Response payload for list_watched_routes."""

    watched_routes: list[WatchedRouteOutput]
    count: int
    summary: str


class TravelPreferencesOutput(BaseModel):
    """The single-user travel preferences record."""

    home_airport: str
    preferred_airlines: list[str]
    max_stops: int
    checked_bag_required: bool
    avoid_overnight_layovers: bool
    preferred_departure_time_range: DepartureTimeRange
    updated_at: str = Field(description="ISO timestamp of the latest update.")
    summary: str
