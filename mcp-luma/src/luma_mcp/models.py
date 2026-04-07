"""Normalized event model shared across all data sources."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventSource(str, Enum):
    API = "api"
    DISCOVER = "discover"
    SUBSCRIPTION = "subscription"


class LumaEvent(BaseModel):
    """Unified event representation produced by all Luma clients."""

    id: str = Field(description="Luma event API id (e.g. evt-...)")
    url: str = Field(description="Canonical event URL (e.g. https://lu.ma/slug)")
    source: EventSource

    title: str
    description: str = ""

    start_at: datetime
    end_at: Optional[datetime] = None
    timezone: Optional[str] = None

    lat: Optional[float] = None
    lon: Optional[float] = None
    city: Optional[str] = None
    location_label: Optional[str] = None
    full_address: Optional[str] = None

    cover_url: Optional[str] = None
    category: Optional[str] = None

    # populated by distance filter
    distance_miles: Optional[float] = None

    @property
    def canonical_url(self) -> str:
        if self.url.startswith("http"):
            return self.url
        return f"https://lu.ma/{self.url}"

    @property
    def has_coordinates(self) -> bool:
        return self.lat is not None and self.lon is not None


def merge_events(event_lists: list[list[LumaEvent]]) -> list[LumaEvent]:
    """Merge multiple event lists, deduplicating by canonical URL."""
    seen: dict[str, LumaEvent] = {}
    for events in event_lists:
        for event in events:
            key = event.canonical_url
            if key not in seen:
                seen[key] = event
    return list(seen.values())
