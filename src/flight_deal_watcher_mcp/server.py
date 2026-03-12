"""Main MCP server entrypoint for Phase 1."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP

from flight_deal_watcher_mcp.config import get_settings
from flight_deal_watcher_mcp.db.repositories import (
    DealAlertsRepository,
    FlightSearchResultsRepository,
    UserPreferencesRepository,
    WatchedRoutesRepository,
)
from flight_deal_watcher_mcp.db.sqlite import create_connection, initialize_database
from flight_deal_watcher_mcp.providers.base import FlightProvider
from flight_deal_watcher_mcp.providers.mock_provider import MockFlightProvider
from flight_deal_watcher_mcp.services.preference_service import PreferenceService
from flight_deal_watcher_mcp.services.watch_service import WatchService
from flight_deal_watcher_mcp.tools import list_watched_routes, search_flights, set_travel_preferences, watch_route
from flight_deal_watcher_mcp.utils.logging import configure_logging, get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class AppContainer:
    """Objects shared across registered MCP tools."""

    connection: sqlite3.Connection
    flight_provider: FlightProvider
    watch_service: WatchService
    preference_service: PreferenceService
    search_results_repository: FlightSearchResultsRepository
    deal_alerts_repository: DealAlertsRepository


def create_container() -> AppContainer:
    """Build the app container used by the MCP server."""
    settings = get_settings()
    configure_logging(settings.log_level)

    connection = create_connection(settings.resolved_db_path)
    initialize_database(connection)

    if settings.provider != "mock":
        raise ValueError(f"Unsupported provider '{settings.provider}'. Phase 1 only supports 'mock'.")

    watched_routes_repository = WatchedRoutesRepository(connection)
    user_preferences_repository = UserPreferencesRepository(connection)

    container = AppContainer(
        connection=connection,
        flight_provider=MockFlightProvider(),
        watch_service=WatchService(watched_routes_repository),
        preference_service=PreferenceService(user_preferences_repository),
        search_results_repository=FlightSearchResultsRepository(connection),
        deal_alerts_repository=DealAlertsRepository(connection),
    )
    LOGGER.info("Initialized app container with SQLite database at %s", settings.resolved_db_path)
    return container


def create_server() -> FastMCP:
    """Create and register the Phase 1 MCP server."""
    container = create_container()
    mcp = FastMCP(
        "flight-deal-watcher-mcp",
        instructions=(
            "A beginner-friendly MCP server for searching mock flights, storing watched routes, "
            "and saving travel preferences."
        ),
    )

    search_flights.register(mcp, flight_provider=container.flight_provider)
    watch_route.register(mcp, watch_service=container.watch_service)
    list_watched_routes.register(mcp, watch_service=container.watch_service)
    set_travel_preferences.register(mcp, preference_service=container.preference_service)

    return mcp


def main() -> None:
    """Run the MCP server using stdio transport."""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
