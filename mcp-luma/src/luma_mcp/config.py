from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    geocoding_provider: str = "nominatim"
    geocoding_api_key: str | None = None
    event_store_path: str | None = None


def load_config() -> Config:
    """Load configuration from environment variables (.env supported)."""
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    return Config(
        geocoding_provider=os.getenv("GEOCODING_PROVIDER", "nominatim").lower(),
        geocoding_api_key=os.getenv("GEOCODING_API_KEY") or None,
        event_store_path=os.getenv("EVENT_STORE_PATH") or None,
    )
