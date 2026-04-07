"""Geocode adapter — resolve a free-text address to (lat, lon).

Default provider: Nominatim (free, no key required).
Optional: Google or Mapbox via GEOCODING_PROVIDER + GEOCODING_API_KEY env.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from geopy.geocoders import GoogleV3, MapBox, Nominatim


@lru_cache(maxsize=256)
def geocode(address: str, *, provider: str = "nominatim", api_key: Optional[str] = None) -> tuple[Optional[float], Optional[float]]:
    """Geocode an address string to (lat, lon). Returns (None, None) on failure."""
    try:
        geocoder = _get_geocoder(provider, api_key)
        location = geocoder.geocode(address, timeout=10)
        if location is None:
            return None, None
        return location.latitude, location.longitude
    except Exception:
        return None, None


def _get_geocoder(provider: str, api_key: Optional[str]):
    provider = provider.lower()
    if provider == "google" and api_key:
        return GoogleV3(api_key=api_key)
    if provider == "mapbox" and api_key:
        return MapBox(api_key=api_key)
    return Nominatim(user_agent="luma-mcp/0.1")
