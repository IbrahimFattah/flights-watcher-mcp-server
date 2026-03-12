"""Implementation of the search_flights MCP tool."""

from __future__ import annotations

from pydantic import ValidationError

from flight_deal_watcher_mcp.providers.base import FlightProvider, ProviderSearchQuery
from flight_deal_watcher_mcp.schemas.tool_inputs import SearchFlightsInput
from flight_deal_watcher_mcp.schemas.tool_outputs import SearchFlightsOutput
from flight_deal_watcher_mcp.services.normalization import build_search_output
from flight_deal_watcher_mcp.utils.validation import format_validation_error


def register(mcp, *, flight_provider: FlightProvider) -> None:
    """Register the search_flights tool on the MCP server."""

    @mcp.tool(name="search_flights", structured_output=True)
    def search_flights(
        origin: str,
        destination: str,
        departure_date: str,
        return_date: str | None = None,
        adults: int = 1,
        cabin: str = "economy",
        nonstop_only: bool = False,
        checked_bag_required: bool = False,
    ) -> SearchFlightsOutput:
        """Search mock flight options and return normalized results."""
        try:
            tool_input = SearchFlightsInput(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                adults=adults,
                cabin=cabin,
                nonstop_only=nonstop_only,
                checked_bag_required=checked_bag_required,
            )
        except ValidationError as error:
            raise ValueError(format_validation_error(error)) from error

        query = ProviderSearchQuery(
            origin=tool_input.origin,
            destination=tool_input.destination,
            departure_date=tool_input.departure_date,
            return_date=tool_input.return_date,
            adults=tool_input.adults,
            cabin=tool_input.cabin,
            nonstop_only=tool_input.nonstop_only,
            checked_bag_required=tool_input.checked_bag_required,
        )
        options = flight_provider.search(query)
        return build_search_output(query, options)
