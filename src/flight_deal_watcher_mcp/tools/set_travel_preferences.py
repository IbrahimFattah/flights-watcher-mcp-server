"""Implementation of the set_travel_preferences MCP tool."""

from __future__ import annotations

from pydantic import ValidationError

from flight_deal_watcher_mcp.schemas.tool_inputs import SetTravelPreferencesInput
from flight_deal_watcher_mcp.schemas.tool_outputs import TravelPreferencesOutput
from flight_deal_watcher_mcp.services.preference_service import PreferenceService
from flight_deal_watcher_mcp.utils.validation import format_validation_error


def register(mcp, *, preference_service: PreferenceService) -> None:
    """Register the set_travel_preferences tool on the MCP server."""

    @mcp.tool(name="set_travel_preferences", structured_output=True)
    def set_travel_preferences(
        home_airport: str,
        preferred_airlines: list[str],
        max_stops: int,
        checked_bag_required: bool,
        avoid_overnight_layovers: bool,
        preferred_departure_time_range: dict[str, str],
    ) -> TravelPreferencesOutput:
        """Store or update a single travel preferences record."""
        try:
            tool_input = SetTravelPreferencesInput(
                home_airport=home_airport,
                preferred_airlines=preferred_airlines,
                max_stops=max_stops,
                checked_bag_required=checked_bag_required,
                avoid_overnight_layovers=avoid_overnight_layovers,
                preferred_departure_time_range=preferred_departure_time_range,
            )
        except ValidationError as error:
            raise ValueError(format_validation_error(error)) from error

        return preference_service.save_preferences(tool_input)
