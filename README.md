# flight-deal-watcher-mcp

A beginner-friendly MCP server built with Python, SQLite, and mock flight data.

Phase 1 focuses on:

- searching mock flights
- saving watched routes
- listing active watched routes
- storing travel preferences

This version does not scrape websites, book flights, or process payments. It is designed to be easy to read, easy to extend, and ready for a future real flight API integration.

## What You Can Do In Phase 1

The server exposes these MCP tools:

- `search_flights`
- `watch_route`
- `list_watched_routes`
- `set_travel_preferences`

The mock provider includes realistic sample routes for:

- `AMM -> DOH`
- `AMM -> IST`
- `AMM -> DXB`

## Project Structure

```text
flight-deal-watcher-mcp/
  README.md
  pyproject.toml
  .env.example
  data/
  src/
    flight_deal_watcher_mcp/
      server.py
      config.py
      db/
      providers/
      schemas/
      services/
      tools/
      utils/
```

## Architecture Overview

The code is split into small layers so it stays understandable:

- `tools/`
  MCP tool handlers. These are the entrypoints your MCP client calls.
- `schemas/`
  Pydantic models for input validation and clean output formatting.
- `providers/`
  The flight provider abstraction and a mock provider used in Phase 1.
- `services/`
  Small business-logic helpers that keep tool files thin.
- `db/`
  SQLite connection helpers, schema creation, and repository classes.
- `utils/`
  Shared helpers for logging, route keys, validation, and time handling.

## Database Tables

Phase 1 creates these SQLite tables:

- `user_preferences`
- `watched_routes`
- `flight_search_results`
- `deal_alerts`

Only the first two are actively used in Phase 1. The other two are created now so Phase 2 can add price-history and deal tracking without reshaping the project.

## Requirements

- Python `3.13`
- `venv`
- internet access for installing Python packages

## Setup

From the project folder:

```bash
cd /Users/ibrahimabdfelfattah/flight-deal-watcher-mcp
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
```

The default `.env.example` values are:

```env
FLIGHT_DEAL_DB_PATH=./data/flight_deal_watcher.db
FLIGHT_DEAL_PROVIDER=mock
LOG_LEVEL=INFO
```

## Running The Server

After activating the virtual environment:

```bash
flight-deal-watcher-mcp
```

Or:

```bash
python -m flight_deal_watcher_mcp.server
```

This runs the MCP server over stdio, which is what Codex and many local MCP clients expect.

## Connecting In Codex

After the environment is ready, add the server to Codex with:

```bash
codex mcp add flight-deal-watcher -- /Users/ibrahimabdfelfattah/flight-deal-watcher-mcp/.venv/bin/python -m flight_deal_watcher_mcp.server
```

You can inspect the saved configuration with:

```bash
codex mcp get flight-deal-watcher --json
```

## Tool Examples

### `search_flights`

Search a one-way route:

```json
{
  "origin": "AMM",
  "destination": "DOH",
  "departure_date": "2026-04-18",
  "adults": 1,
  "cabin": "economy",
  "nonstop_only": false,
  "checked_bag_required": true
}
```

Search a round-trip route:

```json
{
  "origin": "AMM",
  "destination": "IST",
  "departure_date": "2026-05-02",
  "return_date": "2026-05-06",
  "adults": 2,
  "cabin": "economy",
  "nonstop_only": false,
  "checked_bag_required": false
}
```

### `watch_route`

```json
{
  "origin": "AMM",
  "destination": "DXB",
  "earliest_departure": "2026-06-01",
  "latest_departure": "2026-06-10",
  "flex_days": 2,
  "target_price_usd": 190,
  "max_stops": 1
}
```

### `set_travel_preferences`

```json
{
  "home_airport": "AMM",
  "preferred_airlines": ["RJ", "TK"],
  "max_stops": 1,
  "checked_bag_required": true,
  "avoid_overnight_layovers": true,
  "preferred_departure_time_range": {
    "start": "06:00",
    "end": "12:00"
  }
}
```

### `list_watched_routes`

This tool takes no input. It returns all active watched routes from SQLite.

## Validation Rules

Phase 1 includes basic validation:

- airport codes must be three letters like `AMM`
- dates must use `YYYY-MM-DD`
- `return_date` must not be earlier than `departure_date`
- watch date ranges must be ordered correctly
- departure time preferences must use `HH:MM`
- cabin must be one of `economy`, `premium_economy`, `business`, or `first`

## Manual Smoke Test Checklist

After setup, these are the best first tests:

1. Run `search_flights` for `AMM -> DOH` and confirm you get normalized results.
2. Run `search_flights` for `AMM -> IST` with a return date and confirm inbound segments appear.
3. Run `watch_route` for `AMM -> DXB` and confirm a `watch_id` is returned.
4. Run `list_watched_routes` and confirm the saved route appears.
5. Run `set_travel_preferences` and confirm the saved settings come back cleanly.
6. Try an invalid airport code like `AMMA` and confirm the error message is clear.

## How The Mock Provider Works

The provider does not call any external flight API yet.

Instead, it:

- uses route templates stored in `providers/mock_data.py`
- generates real-looking dated itineraries for the requested travel date
- adjusts prices by cabin, trip type, passenger count, and a deterministic date-based variation
- returns clean normalized results through the `services/normalization.py` layer

## Phase 2 Preview

The next phase will add:

- `compare_flights`
- `check_deals`
- `explain_deal`
- MCP resources
- history-aware deal scoring
- automated tests

## Notes For Future Real API Support

When you are ready to integrate a real provider, the main extension points are:

- `providers/base.py`
- `providers/mock_provider.py`
- `services/normalization.py`

The goal is to swap the provider implementation while keeping the tool interfaces and output schema stable.
