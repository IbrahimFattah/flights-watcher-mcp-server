"""Input schemas for MCP tools."""

from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator

from flight_deal_watcher_mcp.utils.validation import (
    normalize_airline_codes,
    normalize_airport_code,
    validate_date_order,
    validate_time_text,
)


class CabinClass(str, Enum):
    """Supported cabin values for flight search."""

    economy = "economy"
    premium_economy = "premium_economy"
    business = "business"
    first = "first"


class DepartureTimeRange(BaseModel):
    """Preferred departure window expressed in local time."""

    start: str = Field(description="Start time in HH:MM format.")
    end: str = Field(description="End time in HH:MM format.")

    @field_validator("start", "end")
    @classmethod
    def validate_time_fields(cls, value: str) -> str:
        """Ensure each value uses HH:MM format."""
        return validate_time_text(value)


class SearchFlightsInput(BaseModel):
    """Validated input for the search_flights tool."""

    origin: str
    destination: str
    departure_date: date
    return_date: date | None = None
    adults: int = Field(default=1, ge=1, le=9)
    cabin: CabinClass = CabinClass.economy
    nonstop_only: bool = False
    checked_bag_required: bool = False

    @field_validator("origin", "destination")
    @classmethod
    def normalize_airport(cls, value: str) -> str:
        """Normalize airport codes to uppercase."""
        return normalize_airport_code(value)

    @model_validator(mode="after")
    def validate_dates(self) -> "SearchFlightsInput":
        """Ensure the return date is not before the departure date."""
        if self.return_date is not None:
            validate_date_order(self.departure_date, self.return_date, "departure_date", "return_date")
        return self


class WatchRouteInput(BaseModel):
    """Validated input for the watch_route tool."""

    origin: str
    destination: str
    earliest_departure: date
    latest_departure: date
    return_earliest: date | None = None
    return_latest: date | None = None
    flex_days: int = Field(default=0, ge=0, le=14)
    target_price_usd: float = Field(gt=0)
    max_stops: int = Field(default=0, ge=0, le=3)

    @field_validator("origin", "destination")
    @classmethod
    def normalize_airport(cls, value: str) -> str:
        """Normalize airport codes to uppercase."""
        return normalize_airport_code(value)

    @model_validator(mode="after")
    def validate_ranges(self) -> "WatchRouteInput":
        """Ensure the watched travel windows are valid."""
        validate_date_order(
            self.earliest_departure,
            self.latest_departure,
            "earliest_departure",
            "latest_departure",
        )
        if (self.return_earliest is None) != (self.return_latest is None):
            raise ValueError("return_earliest and return_latest must be provided together.")
        if self.return_earliest is not None and self.return_latest is not None:
            validate_date_order(
                self.return_earliest,
                self.return_latest,
                "return_earliest",
                "return_latest",
            )
        return self


class SetTravelPreferencesInput(BaseModel):
    """Validated input for the set_travel_preferences tool."""

    home_airport: str
    preferred_airlines: list[str] = Field(default_factory=list)
    max_stops: int = Field(default=1, ge=0, le=3)
    checked_bag_required: bool = False
    avoid_overnight_layovers: bool = False
    preferred_departure_time_range: DepartureTimeRange

    @field_validator("home_airport")
    @classmethod
    def normalize_airport(cls, value: str) -> str:
        """Normalize airport codes to uppercase."""
        return normalize_airport_code(value)

    @field_validator("preferred_airlines")
    @classmethod
    def normalize_airlines(cls, values: list[str]) -> list[str]:
        """Normalize airline codes or short labels."""
        return normalize_airline_codes(values)
