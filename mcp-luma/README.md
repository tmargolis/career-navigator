# Luma Events MCP Server

<!-- mcp-name: io.github.alx1p/luma-mcp -->

A [FastMCP](https://gofastmcp.com) server that discovers events from [Luma](https://luma.com) — combining the Discover feed and subscribed calendars — with distance filtering and ICS export. No API key required for basic discovery.

## How it works

Luma's Discover API has two endpoints that behave very differently:

- **Category search** (e.g. AI, Tech, Food) — returns hundreds of events with rich tagging, but only for your home region. Great depth, geographically locked.
- **City search** (e.g. Paris, London, Tokyo) — returns a curated set of ~20–40 top/featured events for that city. Broad coverage, smaller set.

This MCP uses both via two search modes:

- **Home mode** (default, no `city` param) — searches your preferred categories via the Category API. Deep, rich results filtered by address and distance.
- **Travel mode** (pass a `city`) — fetches the curated top events for that city via the Place API.

On first run, the server returns popular events near you (geo-biased by IP), then walks you through setting up categories, address, and login for progressively richer results.

## Tools

| Tool | What it does |
|------|-------------|
| `search_events` | **Home mode**: search by category with address/distance filtering. **Travel mode**: curated events for a specific city. |
| `set_preferences` | Save default categories (list), address, and max distance. Persists in SQLite across restarts. |
| `get_event` | Fetch full details for a single event by API id or `lu.ma` URL. |
| `export_event_ics` | Generate an ICS string for any event — paste into Apple Calendar, Google Calendar, Outlook, etc. |

## Setup

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Install

```bash
git clone <this-repo>
cd "Luma Cal MCP"
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install -e .
```

### Subscribed calendars (optional)

To access events from calendars you follow on Luma, install the optional auth dependencies:

```bash
uv pip install -e ".[auth]"
playwright install chromium
```

### First run

On first use, the raw Discover feed returns hundreds of popular events near you (geo-biased by IP). The server then walks you through setup one prompt at a time to narrow results:

1. **Address** — asks for your location and preferred search radius, which dramatically reduces the result set to events near you.
2. **Categories** — asks which topics interest you (from: tech, ai, food, arts, climate, fitness, wellness, crypto) for focused discovery.
3. **Login** — asks whether to log in for subscribed calendars.

Each prompt appears after returning results, so you see events immediately. After you configure a preference, the search reruns automatically and the next prompt appears. You can respond "not now" (prompt reappears next time) or "never" (permanently dismissed).

### Configure

Use `set_preferences` to save defaults that persist across restarts:

```
set_preferences(address="3180 18th St, San Francisco", max_distance_miles=15)
set_preferences(categories=["ai", "tech"])
```

### Run

```bash
# stdio transport (for Cursor, Claude Desktop, etc.)
fastmcp run src/luma_mcp/server.py

# or directly
python -m luma_mcp.server
```

## Authentication

Subscribed calendars require a Luma session cookie. The server handles this automatically via an inline login flow.

**How it works:**

1. **First call** — after results, the server prompts for login. The agent asks you in chat.
2. **Login** — the agent calls `search_events` with `login=true`. A Chromium browser opens to `lu.ma/signin`; log in normally. The session cookie is stored in the local SQLite DB.
3. **Decline** — the agent calls `search_events` with `skip_login_days=N` to defer (0 = ask next time, -1 = never).
4. **Returning user, cookie expired** — the browser opens automatically for re-authentication.
5. **Validation** — the stored cookie is validated against Luma's API every 24 hours.

## New Event Tracking

The server maintains a local SQLite database (`~/.luma-mcp/events.db` by default) that records the first time each event is seen. This enables two filters on `search_events`:

- **`added_within_days`** — only return events first seen within the last N days.
- **`new_only`** — only return events that have never been seen before.

Every result also includes `first_seen_at` (ISO timestamp) and `is_new` (boolean).

## Cursor MCP Configuration

Add to your Cursor MCP settings (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "luma-events": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/Luma Cal MCP",
        "fastmcp", "run", "src/luma_mcp/server.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/Luma Cal MCP/src"
      }
    }
  }
}
```

## Data Sources

| Source | Auth | Coverage |
|--------|------|----------|
| **Discover** (`api.lu.ma`) | None required | Public events by city and category — same feed as [luma.com/discover](https://luma.com/discover) |
| **Subscribed calendars** (`api.lu.ma`) | Browser login (auto-managed) | Events from calendars you follow on Luma |

Without logging in, the server still works — Discover is fully available with no authentication.

## Distance Filtering

Set a home address via `set_preferences(address="...")` with `max_distance_miles`. In home mode, events beyond the radius are excluded. Events without location data are included by default (with `distance_miles: null`). In travel mode, distance filtering uses the city center at 25 miles automatically.

Geocoding uses [Nominatim](https://nominatim.org/) (free, OpenStreetMap) by default. For higher volume, set `GEOCODING_PROVIDER=google` or `mapbox` with the corresponding `GEOCODING_API_KEY` in your environment.

## Event Times

Event times (`start_at`, `end_at`) are returned in the user's system timezone. The `timezone` field from Luma is included in every result for reference.

## Limitations

- **RSVP is browser-only.** `get_event` returns the RSVP URL; there's no headless registration path. Use `export_event_ics` to add events to your calendar.
- **Web endpoints are undocumented.** The Discover and subscribed-calendars feeds use Luma's internal API (`api.lu.ma`), which can change without notice. Breakage is isolated to `luma_web_client.py`.
