"""Service helpers for watched route operations."""

from __future__ import annotations

from flight_deal_watcher_mcp.db.models import WatchedRouteRecord
from flight_deal_watcher_mcp.db.repositories import WatchedRoutesRepository
from flight_deal_watcher_mcp.schemas.tool_inputs import WatchRouteInput
from flight_deal_watcher_mcp.schemas.tool_outputs import ListWatchedRoutesOutput, WatchedRouteOutput


class WatchService:
    """Coordinate watched route persistence and formatting."""

    def __init__(self, watched_routes_repository: WatchedRoutesRepository) -> None:
        self.watched_routes_repository = watched_routes_repository

    def create_watch(self, watch_input: WatchRouteInput) -> WatchedRouteOutput:
        """Store a watched route and convert it to the public schema."""
        record = self.watched_routes_repository.create(watch_input)
        return self._to_output(record)

    def list_active(self) -> ListWatchedRoutesOutput:
        """Return all active watched routes."""
        routes = [self._to_output(record) for record in self.watched_routes_repository.list_active()]
        summary = f"Found {len(routes)} active watched route(s)."
        return ListWatchedRoutesOutput(watched_routes=routes, count=len(routes), summary=summary)

    def _to_output(self, record: WatchedRouteRecord) -> WatchedRouteOutput:
        """Convert a repository record into the public watched route schema."""
        summary = (
            f"Watch #{record.watch_id}: {record.origin} -> {record.destination}, "
            f"target ${record.target_price_usd:.2f}, max {record.max_stops} stop(s)."
        )
        return WatchedRouteOutput(
            watch_id=record.watch_id,
            route_key=record.route_key,
            origin=record.origin,
            destination=record.destination,
            earliest_departure=record.earliest_departure,
            latest_departure=record.latest_departure,
            return_earliest=record.return_earliest,
            return_latest=record.return_latest,
            flex_days=record.flex_days,
            target_price_usd=record.target_price_usd,
            max_stops=record.max_stops,
            active=record.active,
            created_at=record.created_at,
            updated_at=record.updated_at,
            summary=summary,
        )
