"""Haversine distance calculation and event filtering."""

from __future__ import annotations

import math

from luma_mcp.models import LumaEvent

EARTH_RADIUS_MILES = 3958.8


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in miles between two (lat, lon) points."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return EARTH_RADIUS_MILES * 2 * math.asin(math.sqrt(a))


def filter_by_distance(
    events: list[LumaEvent],
    center_lat: float,
    center_lon: float,
    max_distance_miles: float,
    *,
    exclude_unknown_location: bool = False,
) -> list[LumaEvent]:
    """Annotate events with distance and drop those beyond the radius."""
    result: list[LumaEvent] = []
    for event in events:
        if not event.has_coordinates:
            if exclude_unknown_location:
                continue
            result.append(event)
            continue

        dist = haversine_miles(center_lat, center_lon, event.lat, event.lon)  # type: ignore[arg-type]
        event = event.model_copy(update={"distance_miles": round(dist, 2)})
        if dist <= max_distance_miles:
            result.append(event)

    return result


def filter_by_keywords(
    events: list[LumaEvent],
    keywords: list[str],
) -> list[LumaEvent]:
    """Keep events whose title or description contains at least one keyword."""
    if not keywords:
        return events

    lower_keywords = [k.lower() for k in keywords]
    result: list[LumaEvent] = []
    for event in events:
        text = f"{event.title} {event.description}".lower()
        if any(kw in text for kw in lower_keywords):
            result.append(event)

    return result

