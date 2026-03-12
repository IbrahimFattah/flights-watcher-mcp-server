"""Implementation of the watch_route MCP tool."""

from __future__ import annotations

from pydantic import ValidationError

from flight_deal_watcher_mcp.schemas.tool_inputs import WatchRouteInput
from flight_deal_watcher_mcp.schemas.tool_outputs import WatchedRouteOutput
from flight_deal_watcher_mcp.services.watch_service import WatchService
from flight_deal_watcher_mcp.utils.validation import format_validation_error


def register(mcp, *, watch_service: WatchService) -> None:
    """Register the watch_route tool on the MCP server."""

    @mcp.tool(name="watch_route", structured_output=True)
    def watch_route(
        origin: str,
        destination: str,
        earliest_departure: str,
        latest_departure: str,
        return_earliest: str | None = None,
        return_latest: str | None = None,
        flex_days: int = 0,
        target_price_usd: float = 0,
        max_stops: int = 0,
    ) -> WatchedRouteOutput:
        """Save a watched route in SQLite and return the created watch."""
        try:
            tool_input = WatchRouteInput(
                origin=origin,
                destination=destination,
                earliest_departure=earliest_departure,
                latest_departure=latest_departure,
                return_earliest=return_earliest,
                return_latest=return_latest,
                flex_days=flex_days,
                target_price_usd=target_price_usd,
                max_stops=max_stops,
            )
        except ValidationError as error:
            raise ValueError(format_validation_error(error)) from error

        return watch_service.create_watch(tool_input)
