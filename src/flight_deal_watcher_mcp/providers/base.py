"""Provider interfaces.

The rest of the application depends on these small dataclasses instead of talking
to a provider-specific response shape directly. That makes a future Postgres
repository or a real flight API easier to plug in.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime

from flight_deal_watcher_mcp.schemas.tool_inputs import CabinClass


@dataclass(slots=True)
class ProviderSearchQuery:
    """The provider-friendly shape of a flight search request."""

    origin: str
    destination: str
    departure_date: date
    return_date: date | None
    adults: int
    cabin: CabinClass
    nonstop_only: bool
    checked_bag_required: bool

    @property
    def is_round_trip(self) -> bool:
        """Return True when the search includes an inbound leg."""
        return self.return_date is not None


@dataclass(slots=True)
class ProviderSegment:
    """One segment returned by a provider implementation."""

    origin: str
    destination: str
    departure_at: datetime
    arrival_at: datetime
    airline: str
    flight_number: str

    @property
    def duration_minutes(self) -> int:
        """Return the segment duration in minutes."""
        return int((self.arrival_at - self.departure_at).total_seconds() // 60)


@dataclass(slots=True)
class ProviderFlightOption:
    """A normalized-enough provider result before final tool formatting."""

    flight_id: str
    provider: str
    primary_airline: str
    cabin: CabinClass
    adults: int
    price_usd: float
    checked_bag_included: bool
    outbound_segments: list[ProviderSegment]
    inbound_segments: list[ProviderSegment] | None

    @property
    def is_round_trip(self) -> bool:
        """Return True when this option includes an inbound itinerary."""
        return bool(self.inbound_segments)

    @property
    def total_stops(self) -> int:
        """Return the total number of connection stops."""
        outbound_stops = max(len(self.outbound_segments) - 1, 0)
        inbound_stops = max(len(self.inbound_segments or []) - 1, 0)
        return outbound_stops + inbound_stops

    @property
    def total_duration_minutes(self) -> int:
        """Return the full itinerary duration in minutes, including layovers."""
        durations = [_itinerary_duration(self.outbound_segments)]
        if self.inbound_segments:
            durations.append(_itinerary_duration(self.inbound_segments))
        return sum(durations)


def _itinerary_duration(segments: list[ProviderSegment]) -> int:
    """Return itinerary duration from first departure to final arrival."""
    if not segments:
        return 0
    return int((segments[-1].arrival_at - segments[0].departure_at).total_seconds() // 60)


class FlightProvider(ABC):
    """Abstract provider interface for flight searches."""

    @abstractmethod
    def search(self, query: ProviderSearchQuery) -> list[ProviderFlightOption]:
        """Return provider flight options for a search request."""
