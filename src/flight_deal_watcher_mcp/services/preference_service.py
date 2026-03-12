"""Service helpers for travel preferences."""

from __future__ import annotations

from flight_deal_watcher_mcp.db.models import TravelPreferencesRecord
from flight_deal_watcher_mcp.db.repositories import UserPreferencesRepository
from flight_deal_watcher_mcp.schemas.tool_inputs import SetTravelPreferencesInput
from flight_deal_watcher_mcp.schemas.tool_outputs import TravelPreferencesOutput


class PreferenceService:
    """Coordinate preferences persistence and output formatting."""

    def __init__(self, user_preferences_repository: UserPreferencesRepository) -> None:
        self.user_preferences_repository = user_preferences_repository

    def save_preferences(self, preferences_input: SetTravelPreferencesInput) -> TravelPreferencesOutput:
        """Store or update the single travel preferences record."""
        record = self.user_preferences_repository.upsert(preferences_input)
        return self._to_output(record)

    def _to_output(self, record: TravelPreferencesRecord) -> TravelPreferencesOutput:
        """Convert a repository record into the public output schema."""
        summary = (
            f"Saved preferences for home airport {record.home_airport} with "
            f"{record.max_stops} max stop(s)."
        )
        return TravelPreferencesOutput(
            home_airport=record.home_airport,
            preferred_airlines=record.preferred_airlines,
            max_stops=record.max_stops,
            checked_bag_required=record.checked_bag_required,
            avoid_overnight_layovers=record.avoid_overnight_layovers,
            preferred_departure_time_range=record.preferred_departure_time_range,
            updated_at=record.updated_at,
            summary=summary,
        )
