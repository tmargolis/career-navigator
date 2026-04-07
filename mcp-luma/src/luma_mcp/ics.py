"""Minimal ICS (iCalendar) builder for a single event."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from luma_mcp.models import LumaEvent


def build_ics(event: LumaEvent) -> str:
    """Return a valid .ics string for one VEVENT."""
    uid = f"{event.id}@luma-mcp"
    now = _ics_dt(datetime.now(tz=timezone.utc))
    dtstart = _ics_dt(event.start_at)
    dtend = _ics_dt(event.end_at) if event.end_at else ""

    location = event.full_address or event.location_label or ""

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//luma-mcp//EN",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{now}",
        f"DTSTART:{dtstart}",
    ]
    if dtend:
        lines.append(f"DTEND:{dtend}")
    lines.append(f"SUMMARY:{_ics_escape(event.title)}")
    if event.description:
        lines.append(f"DESCRIPTION:{_ics_escape(event.description[:500])}")
    if location:
        lines.append(f"LOCATION:{_ics_escape(location)}")
    lines.append(f"URL:{event.canonical_url}")
    lines += [
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    return "\r\n".join(lines) + "\r\n"


def _ics_dt(dt: datetime | str) -> str:
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _ics_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")
