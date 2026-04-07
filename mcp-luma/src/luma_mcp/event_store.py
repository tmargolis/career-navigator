"""Local SQLite store for event tracking and session/settings persistence."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


_DEFAULT_DB_PATH = Path.home() / ".luma-mcp" / "events.db"


class EventStore:
    def __init__(self, db_path: Optional[Path] = None) -> None:
        self._path = db_path or _DEFAULT_DB_PATH
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._path))
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(
            """CREATE TABLE IF NOT EXISTS seen_events (
                event_url   TEXT PRIMARY KEY,
                event_id    TEXT,
                title       TEXT,
                first_seen  TEXT NOT NULL,
                start_at    TEXT
            )"""
        )
        self._migrate_add_start_at()
        self._conn.execute(
            """CREATE TABLE IF NOT EXISTS settings (
                key     TEXT PRIMARY KEY,
                value   TEXT NOT NULL,
                updated TEXT NOT NULL
            )"""
        )
        self._conn.commit()

    def _migrate_add_start_at(self) -> None:
        """Add start_at column to existing databases that lack it."""
        cols = {
            row[1]
            for row in self._conn.execute("PRAGMA table_info(seen_events)").fetchall()
        }
        if "start_at" not in cols:
            self._conn.execute("ALTER TABLE seen_events ADD COLUMN start_at TEXT")
            self._conn.commit()

    def record(self, events: list[dict]) -> list[str]:
        """Record events, returning URLs of newly seen events."""
        now = datetime.now(tz=timezone.utc).isoformat()
        new_urls: list[str] = []
        for ev in events:
            url = ev.get("url", "")
            if not url:
                continue
            start = ev.get("start_at", "")
            try:
                self._conn.execute(
                    "INSERT INTO seen_events (event_url, event_id, title, first_seen, start_at) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (url, ev.get("id", ""), ev.get("title", ""), now, start),
                )
                new_urls.append(url)
            except sqlite3.IntegrityError:
                pass
        self._conn.commit()
        return new_urls

    def prune_past_events(self, before: Optional[datetime] = None) -> int:
        """Delete events whose start_at is before the given datetime.

        Default cutoff is 24 hours ago, not now — this prevents events that
        already started but are still returned by the API from being pruned
        and then re-discovered as "new" on every search.

        Returns the number of deleted rows.
        """
        from datetime import timedelta

        cutoff = (before or datetime.now(tz=timezone.utc) - timedelta(hours=24)).isoformat()
        cursor = self._conn.execute(
            "DELETE FROM seen_events WHERE start_at IS NOT NULL AND start_at < ?",
            (cutoff,),
        )
        self._conn.commit()
        return cursor.rowcount

    def first_seen(self, event_url: str) -> Optional[datetime]:
        row = self._conn.execute(
            "SELECT first_seen FROM seen_events WHERE event_url = ?", (event_url,)
        ).fetchone()
        if row:
            return datetime.fromisoformat(row[0])
        return None

    def first_seen_batch(self, urls: list[str]) -> dict[str, datetime]:
        if not urls:
            return {}
        placeholders = ",".join("?" for _ in urls)
        rows = self._conn.execute(
            f"SELECT event_url, first_seen FROM seen_events WHERE event_url IN ({placeholders})",
            urls,
        ).fetchall()
        return {row[0]: datetime.fromisoformat(row[1]) for row in rows}

    # ------------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------------

    def set_setting(self, key: str, value: str) -> None:
        now = datetime.now(tz=timezone.utc).isoformat()
        self._conn.execute(
            "INSERT INTO settings (key, value, updated) VALUES (?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated = excluded.updated",
            (key, value, now),
        )
        self._conn.commit()

    def get_setting(self, key: str) -> Optional[tuple[str, datetime]]:
        """Return (value, updated) or None."""
        row = self._conn.execute(
            "SELECT value, updated FROM settings WHERE key = ?", (key,)
        ).fetchone()
        if row:
            return row[0], datetime.fromisoformat(row[1])
        return None

    def delete_setting(self, key: str) -> None:
        self._conn.execute("DELETE FROM settings WHERE key = ?", (key,))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
