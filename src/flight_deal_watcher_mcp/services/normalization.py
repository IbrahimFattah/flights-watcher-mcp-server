"""Convert provider responses into clean tool output models."""

from __future__ import annotations

from flight_deal_watcher_mcp.providers.base import ProviderFlightOption, ProviderSearchQuery, ProviderSegment
from flight_deal_watcher_mcp.schemas.tool_outputs import FlightSegmentOutput, NormalizedFlightResult, SearchFlightsOutput
from flight_deal_watcher_mcp.utils.route_keys import build_route_key
from flight_deal_watcher_mcp.utils.time_utils import format_duration


def build_search_output(query: ProviderSearchQuery, options: list[ProviderFlightOption]) -> SearchFlightsOutput:
    """Normalize provider results and wrap them in a search response model."""
    normalized_results = [normalize_flight_option(query, option) for option in options]
    route_text = f"{query.origin} -> {query.destination}"
    summary = f"Found {len(normalized_results)} mock flight option(s) for {route_text}."
    return SearchFlightsOutput(
        origin=query.origin,
        destination=query.destination,
        departure_date=query.departure_date,
        return_date=query.return_date,
        result_count=len(normalized_results),
        results=normalized_results,
        summary=summary,
    )


def normalize_flight_option(query: ProviderSearchQuery, option: ProviderFlightOption) -> NormalizedFlightResult:
    """Convert one provider result into the public normalized result schema."""
    route_key = build_route_key(query.origin, query.destination, query.is_round_trip)
    outbound = [normalize_segment(segment) for segment in option.outbound_segments]
    inbound = [normalize_segment(segment) for segment in option.inbound_segments] if option.inbound_segments else None
    summary = (
        f"{option.primary_airline}, {option.total_stops} stop(s), "
        f"{format_duration(option.total_duration_minutes)}, ${option.price_usd:.2f}"
    )
    return NormalizedFlightResult(
        flight_id=option.flight_id,
        route_key=route_key,
        provider=option.provider,
        cabin=option.cabin,
        adults=option.adults,
        price_usd=option.price_usd,
        checked_bag_included=option.checked_bag_included,
        is_round_trip=option.is_round_trip,
        total_stops=option.total_stops,
        total_duration_minutes=option.total_duration_minutes,
        outbound=outbound,
        inbound=inbound,
        summary=summary,
    )


def normalize_segment(segment: ProviderSegment) -> FlightSegmentOutput:
    """Convert a provider segment into the public segment schema."""
    return FlightSegmentOutput(
        origin=segment.origin,
        destination=segment.destination,
        departure_at=segment.departure_at.isoformat(),
        arrival_at=segment.arrival_at.isoformat(),
        airline=segment.airline,
        flight_number=segment.flight_number,
        duration_minutes=segment.duration_minutes,
        stops=0,
    )
