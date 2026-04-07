"""Luma MCP server — tools for event discovery, details, preferences, and calendar export."""

from __future__ import annotations

import asyncio
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

from luma_mcp.config import Config, load_config
from luma_mcp.event_store import EventStore
from luma_mcp.geo import filter_by_distance, filter_by_keywords
from luma_mcp.geocode import geocode
from luma_mcp.ics import build_ics
from luma_mcp.luma_registry import LumaRegistry
from luma_mcp.luma_web_client import LumaWebClient
from luma_mcp.models import LumaEvent, merge_events

mcp = FastMCP(name="Luma Events")

_config: Optional[Config] = None
_web_client: Optional[LumaWebClient] = None
_web_client_cookie: Optional[str] = None
_event_store: Optional[EventStore] = None
_registry: Optional[LumaRegistry] = None

_VALIDATION_MAX_AGE = timedelta(hours=24)
_NEVER_TIMESTAMP = "9999-12-31T23:59:59+00:00"

def _get_config() -> Config:
    global _config
    if _config is None:
        _config = load_config()
    return _config


def _get_event_store() -> EventStore:
    global _event_store
    if _event_store is None:
        cfg = _get_config()
        db_path = Path(cfg.event_store_path) if cfg.event_store_path else None
        _event_store = EventStore(db_path=db_path)
    return _event_store


def _get_registry() -> LumaRegistry:
    global _registry
    if _registry is None:
        _registry = LumaRegistry(_get_event_store())
    return _registry


def _get_web_client(session_cookie: Optional[str] = None) -> LumaWebClient:
    """Return a LumaWebClient, recreating it if the cookie changed."""
    global _web_client, _web_client_cookie
    if _web_client is None or session_cookie != _web_client_cookie:
        _web_client_cookie = session_cookie
        _web_client = LumaWebClient(session_cookie)
    return _web_client


def _get_stored_cookie(store: EventStore) -> Optional[str]:
    row = store.get_setting("luma_session")
    return row[0] if row else None


def _geocode_fn(address: str) -> tuple[Optional[float], Optional[float]]:
    cfg = _get_config()
    return geocode(address, provider=cfg.geocoding_provider, api_key=cfg.geocoding_api_key)


def _stored_default(store: EventStore, key: str) -> Optional[str]:
    row = store.get_setting(key)
    return row[0] if row else None


# --------------------------------------------------------------------------
# Preference resolution
# --------------------------------------------------------------------------


def _resolve_home_prefs(
    store: EventStore,
) -> tuple[Optional[list[str]], Optional[str], Optional[float]]:
    """Load stored home-mode preferences.

    Returns (default_categories, address, max_distance_miles).
    """
    import json as _json

    cats_raw = _stored_default(store, "default_categories")
    default_categories: Optional[list[str]] = None
    if cats_raw:
        try:
            default_categories = _json.loads(cats_raw)
        except (ValueError, TypeError):
            pass

    address = _stored_default(store, "default_center_address")
    dist_raw = _stored_default(store, "default_max_distance_miles")
    max_dist = float(dist_raw) if dist_raw else None

    return default_categories, address, max_dist


# --------------------------------------------------------------------------
# Session management helpers
# --------------------------------------------------------------------------

async def _resolve_session(
    store: EventStore,
    messages: list[str],
    *,
    login: bool,
    skip_login_days: Optional[int],
) -> tuple[Optional[str], bool]:
    """Determine the session cookie to use for subscribed calendars.

    Returns (cookie, prompted).  ``prompted`` is True when a login prompt was
    added to messages, so callers can defer other prompts.
    """
    # Handle explicit skip_login_days from a prior prompt answer
    if skip_login_days is not None:
        if skip_login_days < 0:
            store.set_setting("luma_login_declined_until", _NEVER_TIMESTAMP)
        elif skip_login_days == 0:
            store.delete_setting("luma_login_declined_until")
        else:
            until = datetime.now(tz=timezone.utc) + timedelta(days=skip_login_days)
            store.set_setting("luma_login_declined_until", until.isoformat())
        return None, False

    # Handle explicit login=true from a prior prompt answer
    if login:
        cookie = await _do_browser_login(store, messages)
        return cookie, False

    # Check if user previously declined and window is still active
    declined_row = store.get_setting("luma_login_declined_until")
    if declined_row:
        declined_until = datetime.fromisoformat(declined_row[0])
        if datetime.now(tz=timezone.utc) < declined_until:
            return None, False
        store.delete_setting("luma_login_declined_until")

    # Try existing cookie
    cookie = _get_stored_cookie(store)
    if cookie:
        valid = await _validate_if_stale(store, cookie, messages)
        if valid:
            return cookie, False
        store.delete_setting("luma_session")
        store.delete_setting("luma_session_validated")

    # No valid cookie — check if user ever logged in before
    had_cookie_row = store.get_setting("luma_login_had_cookie")
    if had_cookie_row and had_cookie_row[0] == "true":
        messages.append(
            "Your Luma session expired. Opening browser to re-authenticate..."
        )
        cookie = await _do_browser_login(store, messages)
        return cookie, False

    # No cookie and never logged in — the login prompt will be handled
    # by the sequential onboarding flow in search_events (third step,
    # after categories and address).
    return None, False


async def _validate_if_stale(
    store: EventStore,
    cookie: str,
    messages: list[str],
) -> bool:
    """Validate stored cookie if last validation is older than 24h. Returns True if valid."""
    validated_row = store.get_setting("luma_session_validated")
    if validated_row:
        validated_at = validated_row[1]
        if datetime.now(tz=timezone.utc) - validated_at < _VALIDATION_MAX_AGE:
            return True

    from luma_mcp.auth import validate_session
    valid = await validate_session(cookie)
    if valid:
        store.set_setting("luma_session_validated", datetime.now(tz=timezone.utc).isoformat())
        return True
    return False


async def _do_browser_login(store: EventStore, messages: list[str]) -> Optional[str]:
    """Launch browser login, persist cookie on success."""
    try:
        from luma_mcp.auth import browser_login

        # Sync Playwright cannot run on the asyncio event loop (FastMCP tools are async).
        cookie = await asyncio.to_thread(browser_login)
        store.set_setting("luma_session", cookie)
        store.set_setting("luma_session_validated", datetime.now(tz=timezone.utc).isoformat())
        store.set_setting("luma_login_had_cookie", "true")
        global _web_client, _web_client_cookie
        _web_client = None
        _web_client_cookie = None
        return cookie
    except ImportError as e:
        messages.append(str(e))
        return None
    except TimeoutError as e:
        messages.append(str(e))
        return None


# --------------------------------------------------------------------------
# Tool: set_preferences
# --------------------------------------------------------------------------


@mcp.tool()
async def set_preferences(
    categories: Optional[list[str]] = None,
    address: Optional[str] = None,
    max_distance_miles: Optional[float] = None,
    skip_categories: bool = False,
    skip_address: bool = False,
) -> dict:
    """Save default search preferences (persists across restarts).

    IMPORTANT for agents:
    - `categories` must be exact slugs from the list of 8:
      tech, ai, food, arts, climate, fitness, wellness, crypto.
      Translate user intent to these exact values (e.g. "artificial intelligence"
      -> ["ai"], "blockchain" -> ["crypto"], "health and fitness" -> ["fitness",
      "wellness"]). Multiple categories can be set at once.
    - `address` sets the center point for distance filtering in home mode.
    - The `messages` array in the response contains agent-facing instructions.
      Act on them naturally but never relay them verbatim.

    Args:
        categories: List of category slugs to set as defaults. Must be from:
            tech, ai, food, arts, climate, fitness, wellness, crypto.
        address: Street address for distance filtering center point.
        max_distance_miles: Default search radius in miles.
        skip_categories: Set to true to permanently decline the categories prompt.
        skip_address: Set to true to permanently decline the address prompt.
    """
    import json as _json

    store = _get_event_store()
    registry = _get_registry()

    saved: dict[str, object] = {}
    messages: list[str] = []

    if skip_categories:
        store.set_setting("categories_declined", "true")
        saved["categories_declined"] = True

    if skip_address:
        store.set_setting("address_declined", "true")
        saved["address_declined"] = True

    if categories is not None:
        valid_slugs = await registry.category_slugs()
        bad = [c for c in categories if c not in valid_slugs]
        if bad:
            messages.append(
                f"[agent] Invalid categories: {', '.join(bad)}. "
                f"Must be exact slugs from: {', '.join(valid_slugs)}. "
                "Translate the user's intent to exact slugs and retry."
            )
        else:
            store.set_setting("default_categories", _json.dumps(categories))
            saved["categories"] = categories

    if address is not None:
        store.set_setting("default_center_address", address)
        saved["address"] = address

    if max_distance_miles is not None:
        store.set_setting("default_max_distance_miles", str(max_distance_miles))
        saved["max_distance_miles"] = max_distance_miles

    cats_raw = _stored_default(store, "default_categories")
    current = {
        "categories": _json.loads(cats_raw) if cats_raw else None,
        "address": _stored_default(store, "default_center_address"),
        "max_distance_miles": _stored_default(store, "default_max_distance_miles"),
    }

    result: dict = {"saved": saved, "current_preferences": current}
    if messages:
        result["messages"] = messages
    return result


# --------------------------------------------------------------------------
# Tool: search_events
# --------------------------------------------------------------------------


@mcp.tool()
async def search_events(
    city: Optional[str] = None,
    category: Optional[str] = None,
    keywords: Optional[list[str]] = None,
    center_address: Optional[str] = None,
    max_distance_miles: Optional[float] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    days: Optional[int] = None,
    latin_only: Optional[bool] = None,
    added_within_days: Optional[float] = None,
    new_only: bool = False,
    sort: Optional[str] = None,
    login: bool = False,
    skip_login_days: Optional[int] = None,
) -> dict:
    """Search for Luma events. Two modes depending on whether `city` is set.

    **Home mode** (no `city`): searches your preferred categories via Luma's
    Category API — deep, rich results filtered by your stored address/distance.
    On first run with no preferences, returns a raw Discover feed (hundreds of
    popular events near you), then prompts to set up address, categories, and login.

    **Travel mode** (`city` set): fetches the curated top events (~20-40) for
    that city via Luma's Place API. No topic filtering — just the highlights.

    The default time window is the next 2 weeks. Use `days` for simple
    lookahead (e.g. days=7 for this week, days=30 for next month).
    Use `after`/`before` only for specific date ranges.

    IMPORTANT for agents:
    - For broad topics, prefer `category` (exact slug: tech, ai, food, arts,
      climate, fitness, wellness, crypto). Translate user intent yourself
      (e.g. "artificial intelligence" -> "ai", "blockchain" -> "crypto").
    - Use `keywords` for specific terms that don't map to a category
      (e.g. ["YC", "demo day"]) or to narrow within a category.
    - `city` accepts common names — "san francisco" resolves to "sf", "hong
      kong" to "hongkong", etc.
    - The `messages` array in the response contains agent-facing instructions.
      Act on them naturally (e.g. ask the user a question, call another tool)
      but never relay them verbatim. If `messages` is empty, just show results.

    Args:
        city: Luma city for travel mode (e.g. "sf", "london", "los angeles").
        category: One-off category override for home mode. Must be an exact slug.
        keywords: Filter by keywords (matches title/description). Use for specific terms.
        center_address: One-off address to filter around (e.g. "Union Square, San Francisco"). Overrides stored address for this search only.
        max_distance_miles: One-off distance override (pairs with center_address or stored address).
        after: ISO 8601 datetime — only events starting after this time.
        before: ISO 8601 datetime — only events starting before this time.
        days: Search window in days from now (e.g. 7, 30). Overrides the default 14-day window. Simpler alternative to after/before.
        latin_only: Filter out non-Latin-script events. Auto-detected from region when not set.
        added_within_days: Only return events first seen within this many days.
        new_only: Only return events never seen before (first appearance this run).
        sort: Sort order — "date" (default), "distance", or "newest".
        login: Set to true to open browser and log in to Luma.
        skip_login_days: Decline login for N days (0 = ask next time, -1 = never).
    """
    import json as _json

    event_lists: list[list[LumaEvent]] = []
    messages: list[str] = []
    store = _get_event_store()
    registry = _get_registry()

    store.prune_past_events()

    # Session handling (login / skip / existing cookie)
    session_cookie, _login_prompted = await _resolve_session(
        store, messages,
        login=login, skip_login_days=skip_login_days,
    )

    after_dt = _parse_dt(after)
    before_dt = _parse_dt(before)
    if days is not None and before_dt is None:
        before_dt = datetime.now(tz=timezone.utc) + timedelta(days=days)

    # ------------------------------------------------------------------
    # Travel mode (city is set)
    # ------------------------------------------------------------------
    if city:
        place_api_id = await registry.resolve_place(city)
        if place_api_id is None:
            match = await registry.match_city(city)
            if match.exact and match.slug:
                city = match.slug
                place_api_id = await registry.resolve_place(city)
            else:
                if match.candidates:
                    options = ", ".join(match.candidates)
                else:
                    place_names = await registry.get_place_names()
                    options = ", ".join(
                        f"{s} ({place_names[s]})" if s in place_names else s
                        for s in await registry.city_slugs()
                    )
                messages.append(
                    f"[agent] \"{city}\" is not a recognized Luma city. "
                    f"Pick the best match and rerun, or clarify with the user.\n"
                    f"Closest: {options}"
                )
                return {"events": [], "count": 0, "messages": messages}

        try:
            web = _get_web_client(session_cookie)
            discover = await web.discover_events(
                place_api_id=place_api_id,
                after=after_dt, before=before_dt,
            )
            event_lists.append(discover)
        except Exception as e:
            messages.append(f"Discover source error: {e}")

        if session_cookie:
            try:
                web = _get_web_client(session_cookie)
                subscribed = await web.subscribed_calendar_events()
                event_lists.append(subscribed)
            except Exception as e:
                messages.append(f"Subscribed calendars error: {e}")

        events = _backfill_known_coords(merge_events(event_lists))

        # City-center distance filter (25mi, exclude unknown coords)
        places = await registry.get_places()
        info = places.get(city)
        if info:
            _pid, clat, clon = info
            events = filter_by_distance(
                events, clat, clon, 25.0, exclude_unknown_location=True,
            )

        # Auto-detect latin_only from continent
        if latin_only is None:
            continent = await registry.continent_of(city)
            latin_only = continent != "apac"

    # ------------------------------------------------------------------
    # Home mode (no city)
    # ------------------------------------------------------------------
    else:
        default_categories, stored_address, stored_dist = _resolve_home_prefs(store)

        eff_dist = max_distance_miles or stored_dist

        # Determine which category API calls to make
        categories_to_fetch: list[str] = []
        if category:
            cat_api_id = await registry.resolve_category(category)
            if cat_api_id is None:
                valid = await registry.category_slugs()
                messages.append(
                    f"[agent] \"{category}\" is not a valid category. "
                    f"Must be one of: {', '.join(valid)}. "
                    "Translate the user's intent to an exact slug and retry."
                )
                return {"events": [], "count": 0, "messages": messages}
            categories_to_fetch = [category]
        elif default_categories:
            categories_to_fetch = default_categories

        web = _get_web_client(session_cookie)

        if categories_to_fetch:
            for cat_slug in categories_to_fetch:
                cat_api_id = await registry.resolve_category(cat_slug)
                if not cat_api_id:
                    continue
                try:
                    cat_events = await web.discover_events(
                        category_api_id=cat_api_id,
                        after=after_dt, before=before_dt,
                    )
                    event_lists.append(cat_events)
                except Exception as e:
                    messages.append(f"Category '{cat_slug}' error: {e}")
        else:
            # Raw Discover feed — no category, no place, just popular near you
            try:
                discover = await web.discover_events(
                    after=after_dt, before=before_dt,
                )
                event_lists.append(discover)
            except Exception as e:
                messages.append(f"Discover source error: {e}")

        if session_cookie:
            try:
                subscribed = await web.subscribed_calendar_events()
                event_lists.append(subscribed)
            except Exception as e:
                messages.append(f"Subscribed calendars error: {e}")

        events = _backfill_known_coords(merge_events(event_lists))

        # Distance filter: one-off center_address overrides stored address
        filter_address = center_address or stored_address
        if filter_address and eff_dist:
            resolved_lat, resolved_lon = _geocode_fn(filter_address)
            if resolved_lat is not None and resolved_lon is not None:
                events = filter_by_distance(
                    events, resolved_lat, resolved_lon, eff_dist,
                )

        if latin_only is None:
            latin_only = True

    # ------------------------------------------------------------------
    # Common post-processing
    # ------------------------------------------------------------------
    if after_dt:
        events = [e for e in events if e.start_at >= after_dt]
    if before_dt:
        events = [e for e in events if e.start_at <= before_dt]

    if keywords:
        events = filter_by_keywords(events, keywords)

    if latin_only:
        events = [e for e in events if _is_latin_event(e)]

    events.sort(key=lambda e: e.start_at)

    summaries = [_event_summary(e) for e in events]

    seen_times = store.first_seen_batch([s["url"] for s in summaries])
    now_iso = datetime.now(tz=timezone.utc).isoformat()

    for s in summaries:
        fs = seen_times.get(s["url"])
        s["first_seen_at"] = fs.isoformat() if fs else now_iso
        s["is_new"] = s["url"] not in seen_times

    if new_only:
        summaries = [s for s in summaries if s["is_new"]]

    if added_within_days is not None:
        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=added_within_days)
        summaries = [
            s for s in summaries
            if s["first_seen_at"] and datetime.fromisoformat(s["first_seen_at"]) >= cutoff
        ]

    if sort == "distance":
        summaries.sort(key=lambda s: s.get("distance_miles", float("inf")))
    elif sort == "newest":
        summaries.sort(key=lambda s: s.get("first_seen_at") or "", reverse=True)

    # Only record events that survive all filters (i.e. will be shown to the user)
    store.record(summaries)

    # ------------------------------------------------------------------
    # Sequential onboarding prompts (one per call, in priority order)
    # ------------------------------------------------------------------
    if not city:
        cats_raw = _stored_default(store, "default_categories")
        has_categories = bool(cats_raw and _json.loads(cats_raw))
        has_address = bool(_stored_default(store, "default_center_address"))
        cats_declined = bool(_stored_default(store, "categories_declined"))
        addr_declined = bool(_stored_default(store, "address_declined"))

        if not has_address and not addr_declined:
            messages.append(
                "[agent] No home address set for distance filtering. Ask the user "
                "for their address and preferred radius, then call "
                "set_preferences(address=\"...\", max_distance_miles=N).\n\n"
                "If the user says 'not now', do nothing.\n"
                "If the user says 'never', call set_preferences(skip_address=true)."
            )
        elif not has_categories and not cats_declined and not category:
            cat_list = ", ".join(await registry.category_slugs())
            messages.append(
                "[agent] No default categories set. Ask the user which topics "
                "interest them. Translate their answer to exact slugs and call "
                f"set_preferences(categories=[...]). Available: {cat_list}\n\n"
                "If the user says 'not now', do nothing (will ask again next time).\n"
                "If the user says 'never', call set_preferences(skip_categories=true)."
            )
        elif not session_cookie and not _login_prompted:
            declined_row = store.get_setting("luma_login_declined_until")
            login_declined = False
            if declined_row:
                declined_until = datetime.fromisoformat(declined_row[0])
                login_declined = datetime.now(tz=timezone.utc) < declined_until
            if not login_declined:
                messages.append(
                    "[agent] Results above are from Luma Discover (public events). "
                    "The user can also log in to see events from calendars they "
                    "follow on Luma, which may surface more results. Ask if they "
                    "want to connect their Luma account.\n\n"
                    "On yes: call search_events with login=true\n"
                    "On no: call search_events with skip_login_days=0\n"
                    "On never: call search_events with skip_login_days=-1"
                )

    return {
        "events": summaries,
        "count": len(summaries),
        "messages": messages or None,
    }


# --------------------------------------------------------------------------
# Tool: get_event
# --------------------------------------------------------------------------


@mcp.tool()
async def get_event(event_id: Optional[str] = None, url: Optional[str] = None) -> dict:
    """Get full details for a single Luma event.

    Args:
        event_id: Luma event API id (e.g. "evt-abc123").
        url: lu.ma event URL or ID (e.g. "https://lu.ma/myevent" or "myevent").
    """
    if not event_id and not url:
        return {"error": "Provide either event_id or url."}

    resolved_id = event_id
    if not resolved_id and url:
        resolved_id = _extract_event_id_from_url(url)

    web = _get_web_client()
    event = await web.get_event(resolved_id)  # type: ignore[arg-type]

    if event is None:
        return {"error": f"Event not found: {event_id or url}"}

    return _event_detail(event)


# --------------------------------------------------------------------------
# Tool: export_event_ics
# --------------------------------------------------------------------------


@mcp.tool()
async def export_event_ics(event_id: Optional[str] = None, url: Optional[str] = None) -> dict:
    """Generate an ICS calendar string for a Luma event (Add to Calendar).

    Args:
        event_id: Luma event API id (e.g. "evt-abc123").
        url: lu.ma event URL or ID.
    """
    detail = await get_event(event_id=event_id, url=url)
    if "error" in detail:
        return detail

    event = LumaEvent(
        id=detail["id"],
        url=detail["url"],
        source=detail["source"],
        title=detail["title"],
        description=detail.get("description", ""),
        start_at=detail["start_at"],
        end_at=detail.get("end_at"),
        timezone=detail.get("timezone"),
        lat=detail.get("lat"),
        lon=detail.get("lon"),
        location_label=detail.get("location_label"),
        full_address=detail.get("full_address"),
        cover_url=detail.get("cover_url"),
    )

    ics_string = build_ics(event)
    return {
        "ics": ics_string,
        "event_title": event.title,
        "event_url": event.canonical_url,
    }


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def _local_dt(dt: datetime, _tz_name: Optional[str] = None) -> str:
    """Format a datetime in the user's system timezone."""
    return dt.astimezone().isoformat()


def _short_date(dt: datetime) -> str:
    """Format a datetime as 'Sat Mar 22, 2pm' in the user's system timezone."""
    local = dt.astimezone()
    minute = local.minute
    if minute:
        time_str = local.strftime("%-I:%M%p").lower()
    else:
        time_str = local.strftime("%-I%p").lower()
    return f"{local.strftime('%a %b %-d')}, {time_str}"


_STATE_ZIP_RE = re.compile(r"^[A-Z]{2}\s+\d{4,5}")


_MAX_TITLE_LEN = 50
_MAX_LOCATION_LEN = 32


def _esc(text: Optional[str], max_len: int = 0) -> Optional[str]:
    """Escape pipe characters and optionally truncate with ellipsis."""
    if text is None:
        return None
    if max_len and len(text) > max_len:
        text = text[:max_len].rstrip() + "…"
    return text.replace("|", "\\|")


def _extract_city(full_address: Optional[str]) -> Optional[str]:
    """Pull the city name from a full address string.

    Handles formats like:
      '123 Main St, Palo Alto, CA 94301, USA' → 'Palo Alto'
      'San Francisco, CA 94102' → 'San Francisco'
      'San Francisco, CA' → 'San Francisco'
      '550 Laguna St, San Francisco + Full Studio' → 'San Francisco'
      'Online' → None
    """
    if not full_address:
        return None
    # Strip anything after '+' (manual venue annotations like "+ Full Studio")
    cleaned = re.split(r"\s*\+\s*", full_address)[0].strip().rstrip(",")
    parts = [p.strip() for p in cleaned.split(",")]
    # Find the part just before a state+zip pattern
    for i in range(1, len(parts)):
        if _STATE_ZIP_RE.match(parts[i]):
            return parts[i - 1]
    # "City, ST" pattern — first part is the city if second looks like a state
    if len(parts) == 2 and len(parts[1].strip()) == 2 and parts[1].strip().isalpha():
        return parts[0]
    # "Street, City" — second part is likely the city if first starts with a digit
    if len(parts) == 2 and parts[0] and parts[0][0].isdigit():
        return parts[1]
    # 3+ parts without state+zip: second-to-last is likely the city
    if len(parts) >= 3:
        return parts[-2]
    return None


_KnownVenue = tuple[str, float, float]  # (display_name, lat, lon)

_KNOWN_VENUES: dict[str, _KnownVenue] = {
    "550 laguna st": ("The Commons", 37.7764, -122.4225),
    "540 laguna st": ("The Commons", 37.7764, -122.4225),
}


def _venue_name(label: Optional[str]) -> Optional[str]:
    """Return the venue name, or None if it looks like a bare street address."""
    if not label:
        return None
    stripped = label.strip()
    lower = stripped.lower()
    for prefix, (name, _lat, _lon) in _KNOWN_VENUES.items():
        if lower.startswith(prefix):
            return name
    if stripped and stripped[0].isdigit():
        return None
    return stripped


def _backfill_known_coords(events: list[LumaEvent]) -> list[LumaEvent]:
    """Fill in lat/lon for events at known venues that lack coordinates."""
    result: list[LumaEvent] = []
    for ev in events:
        if not ev.has_coordinates and ev.location_label:
            lower = ev.location_label.strip().lower()
            for prefix, (_name, lat, lon) in _KNOWN_VENUES.items():
                if lower.startswith(prefix):
                    ev = ev.model_copy(update={"lat": lat, "lon": lon})
                    break
        result.append(ev)
    return result


def _event_summary(event: LumaEvent) -> dict:
    venue = _venue_name(event.location_label)
    city = event.city or _extract_city(event.full_address) or _extract_city(event.location_label)
    addr_lower = (event.full_address or "").lower()
    label_lower = (event.location_label or "").lower()
    if "online" in addr_lower or "online" in label_lower:
        location = "Online"
    elif venue and city:
        max_venue = _MAX_LOCATION_LEN - len(city) - 2  # room for ", City"
        truncated_venue = _esc(venue, max(max_venue, 10))
        location = f"{truncated_venue}, {city}"
    elif venue:
        location = _esc(venue, _MAX_LOCATION_LEN)
    else:
        location = city

    d: dict = {
        "id": event.id,
        "title": _esc(event.title, _MAX_TITLE_LEN),
        "date": _short_date(event.start_at),
        "start_at": _local_dt(event.start_at, event.timezone),
        "end_at": _local_dt(event.end_at, event.timezone) if event.end_at else None,
        "timezone": event.timezone,
        "location": _esc(location) if location else None,
        "url": event.canonical_url,
    }
    if event.distance_miles is not None:
        d["distance_miles"] = event.distance_miles
    return d


def _event_detail(event: LumaEvent) -> dict:
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "start_at": _local_dt(event.start_at, event.timezone),
        "end_at": _local_dt(event.end_at, event.timezone) if event.end_at else None,
        "timezone": event.timezone,
        "city": event.city or _extract_city(event.full_address) or _extract_city(event.location_label),
        "lat": event.lat,
        "lon": event.lon,
        "location_label": event.location_label,
        "full_address": event.full_address,
        "cover_url": event.cover_url,
        "url": event.canonical_url,
        "rsvp_url": event.canonical_url,
        "source": event.source.value,
    }


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    """Parse an ISO 8601 string, defaulting to UTC if no timezone is given."""
    if not value:
        return None
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _latin_ratio(text: str) -> float:
    """Return the fraction of alphabetic characters that are Latin-script."""
    alpha = [c for c in text if c.isalpha()]
    if not alpha:
        return 1.0
    return sum(1 for c in alpha if c < "\u0250") / len(alpha)


def _has_cjk(text: str) -> bool:
    """Return True if text contains any CJK Unified Ideograph characters."""
    return any("\u4e00" <= c <= "\u9fff" for c in text)


def _is_latin_event(event: LumaEvent) -> bool:
    """Return True if an event appears to be in a Latin-script language.

    Checks title at a strict threshold (brand names like 'OpenAI' inflate
    Latin counts in otherwise non-Latin titles). If a description exists,
    it's checked separately — a non-Latin description filters the event
    even when the title looks Latin. Titles containing CJK characters
    require a higher ratio to pass.
    """
    title_ratio = _latin_ratio(event.title)
    title_threshold = 0.9 if _has_cjk(event.title) else 0.8
    if title_ratio < title_threshold:
        return False
    if event.description and _latin_ratio(event.description) < 0.5:
        return False
    return True


def _extract_event_id_from_url(url: str) -> str:
    """Extract event api_id or slug from a lu.ma URL or bare slug."""
    url = url.strip()
    if url.startswith("http"):
        parts = url.rstrip("/").split("/")
        return parts[-1]
    return url


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
