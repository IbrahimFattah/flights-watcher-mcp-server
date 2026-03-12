"""Implementation of the list_watched_routes MCP tool."""

from __future__ import annotations

from flight_deal_watcher_mcp.schemas.tool_outputs import ListWatchedRoutesOutput
from flight_deal_watcher_mcp.services.watch_service import WatchService


def register(mcp, *, watch_service: WatchService) -> None:
    """Register the list_watched_routes tool on the MCP server."""

    @mcp.tool(name="list_watched_routes", structured_output=True)
    def list_watched_routes() -> ListWatchedRoutesOutput:
        """Return all active watched routes."""
        return watch_service.list_active()
