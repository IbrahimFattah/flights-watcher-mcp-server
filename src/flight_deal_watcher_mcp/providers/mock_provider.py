"""Mock flight provider used in Phase 1."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date

from flight_deal_watcher_mcp.providers.base import FlightProvider, ProviderFlightOption, ProviderSearchQuery, ProviderSegment
from flight_deal_watcher_mcp.providers.mock_data import MOCK_ROUTE_TEMPLATES
from flight_deal_watcher_mcp.schemas.tool_inputs import CabinClass
from flight_deal_watcher_mcp.utils.time_utils import combine_date_and_time

CABIN_PRICE_MULTIPLIERS: dict[CabinClass, float] = {
    CabinClass.economy: 1.0,
    CabinClass.premium_economy: 1.35,
    CabinClass.business: 2.6,
    CabinClass.first: 4.2,
}


@dataclass(slots=True)
class _ResolvedTemplate:
    """A route template resolved to the search direction."""

    template_id: str
    primary_airline: str
    checked_bag_included: bool
    base_price_usd: float
    outbound_segments: list[dict[str, object]]
    inbound_segments: list[dict[str, object]]


class MockFlightProvider(FlightProvider):
    """Return deterministic mock flight results for a small set of routes."""

    provider_name = "mock"

    def search(self, query: ProviderSearchQuery) -> list[ProviderFlightOption]:
        """Return mock results that vary slightly by date and cabin."""
        templates = self._resolve_templates(query.origin, query.destination)
        options: list[ProviderFlightOption] = []

        for template in templates:
            outbound_segments = self._build_segments(template.outbound_segments, query.departure_date)
            inbound_segments = None
            if query.return_date is not None:
                inbound_segments = self._build_segments(template.inbound_segments, query.return_date)

            option = ProviderFlightOption(
                flight_id=self._build_flight_id(template.template_id, query),
                provider=self.provider_name,
                primary_airline=template.primary_airline,
                cabin=query.cabin,
                adults=query.adults,
                price_usd=self._calculate_price(template.base_price_usd, query, template.template_id),
                checked_bag_included=template.checked_bag_included,
                outbound_segments=outbound_segments,
                inbound_segments=inbound_segments,
            )

            if query.nonstop_only and option.total_stops > 0:
                continue
            if query.checked_bag_required and not option.checked_bag_included:
                continue
            options.append(option)

        return sorted(options, key=lambda option: (option.price_usd, option.total_duration_minutes))

    def _resolve_templates(self, origin: str, destination: str) -> list[_ResolvedTemplate]:
        """Return templates for the requested direction."""
        direct_templates = MOCK_ROUTE_TEMPLATES.get((origin, destination))
        if direct_templates is not None:
            return [self._to_resolved_template(template) for template in direct_templates]

        reverse_templates = MOCK_ROUTE_TEMPLATES.get((destination, origin))
        if reverse_templates is None:
            return []

        resolved_templates: list[_ResolvedTemplate] = []
        for template in reverse_templates:
            resolved_templates.append(
                _ResolvedTemplate(
                    template_id=str(template["template_id"]),
                    primary_airline=str(template["primary_airline"]),
                    checked_bag_included=bool(template["checked_bag_included"]),
                    base_price_usd=float(template["base_price_usd"]),
                    outbound_segments=list(template["inbound_segments"]),
                    inbound_segments=list(template["outbound_segments"]),
                )
            )
        return resolved_templates

    def _to_resolved_template(self, template: dict[str, object]) -> _ResolvedTemplate:
        """Convert a raw route template dictionary into a typed helper object."""
        return _ResolvedTemplate(
            template_id=str(template["template_id"]),
            primary_airline=str(template["primary_airline"]),
            checked_bag_included=bool(template["checked_bag_included"]),
            base_price_usd=float(template["base_price_usd"]),
            outbound_segments=list(template["outbound_segments"]),
            inbound_segments=list(template["inbound_segments"]),
        )

    def _build_segments(self, segment_templates: list[dict[str, object]], travel_date: date) -> list[ProviderSegment]:
        """Create dated provider segments from reusable templates."""
        segments: list[ProviderSegment] = []
        for segment_template in segment_templates:
            departure_at = combine_date_and_time(travel_date, str(segment_template["departure_time"]))
            arrival_at = departure_at + _minutes_to_delta(int(segment_template["duration_minutes"]))
            segments.append(
                ProviderSegment(
                    origin=str(segment_template["origin"]),
                    destination=str(segment_template["destination"]),
                    departure_at=departure_at,
                    arrival_at=arrival_at,
                    airline=str(segment_template["airline"]),
                    flight_number=str(segment_template["flight_number"]),
                )
            )
        return segments

    def _calculate_price(self, base_price_usd: float, query: ProviderSearchQuery, template_id: str) -> float:
        """Apply deterministic cabin and date variation to a base price."""
        multiplier = CABIN_PRICE_MULTIPLIERS[query.cabin]
        variation = self._deterministic_variation(query, template_id)
        weekend_factor = 0.08 if query.departure_date.weekday() in {4, 5} else 0.0
        round_trip_factor = 1.82 if query.is_round_trip else 1.0
        adjusted_price = base_price_usd * multiplier * variation * round_trip_factor * query.adults
        adjusted_price *= 1 + weekend_factor
        return round(adjusted_price, 2)

    def _deterministic_variation(self, query: ProviderSearchQuery, template_id: str) -> float:
        """Return a stable multiplier between 0.90 and 1.10 for repeatable mock data."""
        fingerprint = "|".join(
            [
                query.origin,
                query.destination,
                query.departure_date.isoformat(),
                query.return_date.isoformat() if query.return_date else "none",
                query.cabin.value,
                template_id,
            ]
        )
        digest = hashlib.md5(fingerprint.encode("utf-8")).hexdigest()
        offset = int(digest[:2], 16) % 21
        return 0.90 + (offset / 100)

    def _build_flight_id(self, template_id: str, query: ProviderSearchQuery) -> str:
        """Create a stable mock flight identifier."""
        parts = [template_id, query.departure_date.isoformat()]
        if query.return_date is not None:
            parts.append(query.return_date.isoformat())
        parts.append(query.cabin.value)
        return "-".join(parts)


def _minutes_to_delta(duration_minutes: int):
    """Small helper to avoid importing timedelta repeatedly in the class."""
    from datetime import timedelta

    return timedelta(minutes=duration_minutes)
