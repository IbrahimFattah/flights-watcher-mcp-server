"""Validation helpers shared by schema models."""

from __future__ import annotations

import re
from datetime import date, time

from pydantic import ValidationError

AIRPORT_CODE_PATTERN = re.compile(r"^[A-Z]{3}$")
TIME_TEXT_PATTERN = re.compile(r"^\d{2}:\d{2}$")


def normalize_airport_code(value: str) -> str:
    """Normalize an airport code and validate the basic IATA-like shape."""
    normalized = value.strip().upper()
    if not AIRPORT_CODE_PATTERN.fullmatch(normalized):
        raise ValueError("Airport codes must be exactly 3 letters, like AMM or DXB.")
    return normalized


def normalize_airline_codes(values: list[str]) -> list[str]:
    """Normalize airline codes or short airline names to uppercase strings."""
    normalized_values: list[str] = []
    for value in values:
        cleaned = value.strip().upper()
        if not cleaned:
            continue
        normalized_values.append(cleaned)
    return normalized_values


def validate_date_order(start_date: date, end_date: date, start_label: str, end_label: str) -> None:
    """Ensure a start date is not later than its paired end date."""
    if end_date < start_date:
        raise ValueError(f"{end_label} must be on or after {start_label}.")


def validate_time_text(value: str) -> str:
    """Validate a HH:MM value and normalize it."""
    cleaned = value.strip()
    if not TIME_TEXT_PATTERN.fullmatch(cleaned):
        raise ValueError("Time values must use HH:MM format, for example 06:00.")
    time.fromisoformat(cleaned)
    return cleaned


def format_validation_error(error: ValidationError) -> str:
    """Return a friendly one-line validation error message."""
    return "; ".join(detail["msg"] for detail in error.errors(include_url=False))
