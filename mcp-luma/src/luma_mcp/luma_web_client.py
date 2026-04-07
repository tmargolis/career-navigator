"""Client for Luma's internal web API (api.lu.ma).

Discover endpoints work without auth.  Subscribed-calendars require
an authenticated session cookie.  Both are undocumented and may change
without notice — all parsing is isolated in this module.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

import httpx

from luma_mcp.models import EventSource, LumaEvent

_DEFAULT_WINDOW_DAYS = 14
_MAX_PAGES = 40
_PAGE_SIZE = 50

BASE_URL = "https://api.lu.ma"


class LumaWebClient:
    def __init__(self, session_cookie: Optional[str] = None) -> None:
        headers: dict[str, str] = {
            "accept": "application/json",
            "origin": "https://lu.ma",
            "referer": "https://lu.ma/",
        }
        if session_cookie:
            if "=" in session_cookie:
                headers["cookie"] = session_cookie
            else:
                headers["cookie"] = f"luma.auth-session-key={session_cookie}"
        self._client = httpx.AsyncClient(
            base_url=BASE_URL, headers=headers, timeout=30.0
        )
        self._has_session = bool(session_cookie)

    # ------------------------------------------------------------------
    # Discover
    # ------------------------------------------------------------------

    async def discover_events(
        self,
        *,
        place_api_id: Optional[str] = None,
        category_api_id: Optional[str] = None,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None,
    ) -> list[LumaEvent]:
        """Fetch events from the Discover feed (no auth required).

        Paginates automatically until ``before`` is reached.  Defaults to
        a ~30-day window from ``after`` (or now) when ``before`` is not set.
        """
        now = datetime.now(tz=timezone.utc)
        effective_after = _ensure_utc(after) if after else now
        effective_before = _ensure_utc(before) if before else (effective_after + timedelta(days=_DEFAULT_WINDOW_DAYS))

        events: list[LumaEvent] = []
        cursor: Optional[str] = None

        for _ in range(_MAX_PAGES):
            params: dict[str, str | int] = {"pagination_limit": _PAGE_SIZE}
            if place_api_id:
                params["discover_place_api_id"] = place_api_id
            if category_api_id:
                params["discover_category_api_id"] = category_api_id
            if cursor:
                params["pagination_cursor"] = cursor

            resp = await self._client.get(
                "/discover/get-paginated-events", params=params
            )
            resp.raise_for_status()
            data = resp.json()

            page_past_window = False
            for entry in data.get("entries", []):
                ev = _parse_web_event(entry, source=EventSource.DISCOVER)
                if ev is None:
                    continue
                if ev.start_at.astimezone(timezone.utc) > effective_before:
                    page_past_window = True
                    break
                events.append(ev)

            if page_past_window or not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
            if not cursor:
                break

        return events

    # ------------------------------------------------------------------
    # Subscribed calendars
    # ------------------------------------------------------------------

    async def subscribed_calendar_events(
        self,
        *,
        limit: int = 50,
        max_pages: int = 5,
    ) -> list[LumaEvent]:
        """Fetch events from calendars the user subscribes to (requires session)."""
        if not self._has_session:
            return []

        resp = await self._client.get("/home/get-subscribed-calendars")
        if resp.status_code in (401, 403, 404):
            return []
        resp.raise_for_status()
        data = resp.json()

        calendar_ids: list[str] = []
        for entry in data.get("infos", []):
            cal = entry.get("calendar", {})
            cal_id = cal.get("api_id")
            if cal_id:
                calendar_ids.append(cal_id)

        if not calendar_ids:
            return []

        events: list[LumaEvent] = []
        for cal_id in calendar_ids:
            cal_events = await self._calendar_upcoming_events(
                cal_id, limit=limit, max_pages=max_pages
            )
            events.extend(cal_events)

        return events

    async def _calendar_upcoming_events(
        self,
        calendar_api_id: str,
        *,
        limit: int = 50,
        max_pages: int = 3,
    ) -> list[LumaEvent]:
        """Fetch upcoming events for a single calendar via the web API."""
        events: list[LumaEvent] = []
        cursor: Optional[str] = None

        for _ in range(max_pages):
            params: dict[str, str | int] = {
                "calendar_api_id": calendar_api_id,
                "pagination_limit": limit,
            }
            if cursor:
                params["pagination_cursor"] = cursor

            resp = await self._client.get(
                "/calendar/get-items", params=params
            )
            if resp.status_code in (401, 403, 404):
                break
            resp.raise_for_status()
            data = resp.json()

            for entry in data.get("entries", []):
                ev = _parse_web_event(entry, source=EventSource.SUBSCRIPTION)
                if ev:
                    events.append(ev)

            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
            if not cursor:
                break

        return events

    # ------------------------------------------------------------------
    # Single event
    # ------------------------------------------------------------------

    async def get_event(self, event_api_id: str) -> Optional[LumaEvent]:
        """Fetch a single event by API id via the web API (no auth needed)."""
        resp = await self._client.get(
            "/event/get", params={"event_api_id": event_api_id}
        )
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = resp.json()
        event_data = data.get("event", {})
        if not event_data:
            return None

        description = _extract_description_mirror(data.get("description_mirror"))

        return _parse_web_event(
            {"event": event_data, "api_id": data.get("api_id", event_data.get("api_id", ""))},
            source=EventSource.DISCOVER,
            description_override=description,
        )

    async def close(self) -> None:
        await self._client.aclose()


# ------------------------------------------------------------------
# Parsing helpers (web API field names differ from the official API)
# ------------------------------------------------------------------


def _ensure_utc(dt: datetime) -> datetime:
    """Ensure a datetime is timezone-aware, defaulting to UTC if naive."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def _extract_description_mirror(node: dict | list | None) -> str:
    """Extract plain text from a ProseMirror description_mirror document."""
    if not node:
        return ""
    parts: list[str] = []
    if isinstance(node, dict):
        if node.get("type") == "text":
            parts.append(node.get("text", ""))
        for child in node.get("content", []):
            parts.append(_extract_description_mirror(child))
    elif isinstance(node, list):
        for item in node:
            parts.append(_extract_description_mirror(item))
    return " ".join(p for p in parts if p).strip()


def _parse_web_event(
    entry: dict,
    *,
    source: EventSource,
    description_override: str = "",
) -> Optional[LumaEvent]:
    ev = entry.get("event", {})
    if not ev:
        return None

    api_id = ev.get("api_id") or entry.get("api_id", "")
    if not api_id:
        return None

    geo = ev.get("geo_address_info") or {}
    coord = ev.get("coordinate") or {}

    url_slug = ev.get("url", "")

    description = (
        description_override
        or ev.get("description")
        or ev.get("description_md")
        or ""
    )

    return LumaEvent(
        id=api_id,
        url=url_slug,
        source=source,
        title=ev.get("name", ""),
        description=description,
        start_at=ev["start_at"],
        end_at=ev.get("end_at"),
        timezone=ev.get("timezone"),
        lat=coord.get("latitude"),
        lon=coord.get("longitude"),
        city=geo.get("city"),
        location_label=geo.get("address") or geo.get("description"),
        full_address=geo.get("full_address"),
        cover_url=ev.get("cover_url"),
    )
