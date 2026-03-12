"""Time and date helpers for mock flight generation."""

from __future__ import annotations

from datetime import date, datetime, timedelta


def combine_date_and_time(travel_date: date, time_text: str) -> datetime:
    """Create a local datetime from an ISO date and a HH:MM time string."""
    return datetime.fromisoformat(f"{travel_date.isoformat()}T{time_text}:00")


def combine_with_duration(travel_date: date, departure_time: str, duration_minutes: int) -> tuple[datetime, datetime]:
    """Create departure and arrival datetimes from a duration."""
    departure_at = combine_date_and_time(travel_date, departure_time)
    arrival_at = departure_at + timedelta(minutes=duration_minutes)
    return departure_at, arrival_at


def format_duration(duration_minutes: int) -> str:
    """Return a human-friendly duration like 3h 25m."""
    hours, minutes = divmod(duration_minutes, 60)
    if hours and minutes:
        return f"{hours}h {minutes}m"
    if hours:
        return f"{hours}h"
    return f"{minutes}m"
