"""Helpers for building stable route identifiers."""

from __future__ import annotations


def build_route_key(origin: str, destination: str, is_round_trip: bool) -> str:
    """Build a simple route key used by tools and persistence layers."""
    trip_kind = "rt" if is_round_trip else "ow"
    return f"{origin.upper()}-{destination.upper()}-{trip_kind}"
