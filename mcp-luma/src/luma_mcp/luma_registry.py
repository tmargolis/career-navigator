"""Dynamic registry of Luma discover places and categories.

Fetches the canonical list from lu.ma/discover's embedded __NEXT_DATA__,
caches in SQLite, and falls back to a hardcoded snapshot when the fetch
fails or hasn't been attempted yet.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import httpx

from luma_mcp.event_store import EventStore

_CACHE_TTL = timedelta(days=7)
_SETTINGS_KEY_PLACES = "registry_places"
_SETTINGS_KEY_CATEGORIES = "registry_categories"
_SETTINGS_KEY_CONTINENTS = "registry_continents"
_SETTINGS_KEY_PLACE_NAMES = "registry_place_names"
_SETTINGS_KEY_CATEGORY_NAMES = "registry_category_names"

PlaceInfo = tuple[str, float, float]  # (discover_place_api_id, lat, lon)


# ------------------------------------------------------------------
# Hardcoded fallback (snapshot from 2026-03-22)
# ------------------------------------------------------------------

_FALLBACK_PLACES: dict[str, PlaceInfo] = {
    "sf": ("discplace-BDj7GNbGlsF7Cka", 37.7749, -122.4194),
    "la": ("discplace-OgfEAh5KgfMzise", 34.0522, -118.2437),
    "las-vegas": ("discplace-RF9Yq9JDUxmcpTr", 36.2333, -115.2654),
    "sd": ("discplace-MNBATdzid940kqJ", 32.8313, -117.1222),
    "portland": ("discplace-HthnjGVBzGh90sQ", 45.5231, -122.6765),
    "salt-lake-city": ("discplace-gxZJbB572Ls8RRu", 40.7776, -111.9311),
    "phoenix": ("discplace-Vk9M1gTb4AMVXuD", 33.5722, -112.0892),
    "seattle": ("discplace-FQ4E58PeBMHGTKK", 47.6061, -122.3328),
    "vancouver": ("discplace-4fa7ldlAkBTTivm", 49.2827, -123.1207),
    "denver": ("discplace-I94ZmQKKyVnCQKv", 39.762, -104.8758),
    "calgary": ("discplace-7AxSBoZHQy3igIZ", 51.05, -114.0667),
    "dallas": ("discplace-Ez9iuaZfs6AZDls", 32.7935, -96.7667),
    "austin": ("discplace-0tPy8KGz3xMycnt", 30.2672, -97.7413),
    "minneapolis": ("discplace-IHi0OqR5c6t4Hb3", 44.9635, -93.2678),
    "houston": ("discplace-aQeJaEtqg3shHZ1", 29.786, -95.3885),
    "chicago": ("discplace-NdGm35qFD0vaXNF", 41.8375, -87.6866),
    "mexico-city": ("discplace-ntiNB0E437TyRqt", 19.4326, -99.1332),
    "atlanta": ("discplace-C6hWuH5suHJIUqC", 33.7628, -84.422),
    "waterloo_ca": ("discplace-idpnif8MiNuyYI7", 43.4643, -80.5204),
    "toronto": ("discplace-Cx3JMS6vXKAbhV5", 43.6511, -79.347),
    "honolulu": ("discplace-Ce0yAAavKebPHcB", 21.3294, -157.846),
    "dc": ("discplace-AANPgOymN6bqFn8", 38.9047, -77.0163),
    "philadelphia": ("discplace-VGLZZfVwOKRD1Yd", 40.0077, -75.1339),
    "montreal": ("discplace-CXKKcJmNkbj6ikW", 45.5089, -73.5617),
    "nyc": ("discplace-Izx1rQVSh8njYpP", 40.7306, -73.9352),
    "miami": ("discplace-fSrrRYurTwydAGK", 25.784, -80.2101),
    "boston": ("discplace-VWeZ1zUvnawYHMj", 42.3188, -71.0852),
    "medellin": ("discplace-K11Mq0Pw6sbManZ", 6.2308, -75.5906),
    "bogota": ("discplace-Rac9aE9RdKypLVS", 4.7111, -74.0722),
    "buenos-aires": ("discplace-wX2J5xGwAJpznew", -34.5997, -58.3819),
    "saopaulo": ("discplace-AQZnCu9wl4LmOIp", -23.5558, -46.6396),
    "rio": ("discplace-EWglyhh4fsHKo2F", -22.9068, -43.1729),
    "dublin": ("discplace-ffI8KmAB4gC5LMC", 53.35, -6.2603),
    "london": ("discplace-QCcNk3HXowOR97j", 51.5099, -0.1181),
    "stockholm": ("discplace-e7EG0Ef6S2aQnvN", 59.3294, 18.0686),
    "helsinki": ("discplace-gEii5B2Ju5KKRNH", 60.1708, 24.9375),
    "amsterdam": ("discplace-FC4SDMUVXiFtMOr", 52.3728, 4.8936),
    "copenhagen": ("discplace-CmmHAjPdBSsqmJf", 55.6761, 12.5683),
    "brussels": ("discplace-CMxOe3Mv06uUk7l", 50.8467, 4.3525),
    "hamburg": ("discplace-xZzD6rDcDK12oi7", 53.55, 10.0),
    "paris": ("discplace-NdLrh1xJfeotJZC", 48.8566, 2.3522),
    "berlin": ("discplace-gCfX0s3E9Hgo3rG", 52.52, 13.405),
    "lisbon": ("discplace-mgGFFo5EDdyekyE", 38.7253, -9.15),
    "madrid": ("discplace-03jiEcS4mvwJuDa", 40.4168, -3.7038),
    "lausanne": ("discplace-SmrXTBH5rgPvd1h", 46.5197, 6.6323),
    "geneva": ("discplace-RnVxN1SH4HYTeqF", 46.2044, 6.1432),
    "zurich": ("discplace-tSRc3NkTycobe0w", 47.3769, 8.5417),
    "prague": ("discplace-6xx9LRci5NFgdJ5", 50.0875, 14.4214),
    "warsaw": ("discplace-PTcuEQVHuySJe8N", 52.2297, 21.0122),
    "munich": ("discplace-P00kEGGGHNLEYGe", 48.1375, 11.575),
    "barcelona": ("discplace-WcS4REeayDPXV4n", 41.3874, 2.1686),
    "milan": ("discplace-9AyCYUvGH7xiqhh", 45.4669, 9.19),
    "vienna": ("discplace-3YgdIjqj7Pveid3", 48.2081, 16.3713),
    "budapest": ("discplace-zS3rBqHSdNGTSZB", 47.4925, 19.0514),
    "rome": ("discplace-CLGg2G8Q96daz0w", 41.8931, 12.4828),
    "istanbul": ("discplace-0vKyo1D6kdT4ml6", 41.0136, 28.955),
    "tokyo": ("discplace-9H7asQEvWiv6DA9", 35.6764, 139.65),
    "seoul": ("discplace-eQieweHXBFCWbCj", 37.5519, 126.9918),
    "taipei": ("discplace-fi7MDZq99wfKWfa", 25.0375, 121.5625),
    "hongkong": ("discplace-z9B5Guglh2WINA1", 22.3, 114.2),
    "manila": ("discplace-XeAvnK62YmCW54R", 14.5958, 120.9772),
    "ho-chi-minh-city": ("discplace-3ixpMOGpQaA4dWG", 10.7756, 106.7019),
    "bangkok": ("discplace-1bk5q2gBJbv7Ngw", 13.7525, 100.4942),
    "kuala-lumpur": ("discplace-O15L1VZiYe0GYGm", 3.1478, 101.6953),
    "singapore": ("discplace-mUbtdfNjfWaLQ72", 1.2903, 103.852),
    "jakarta": ("discplace-D0vMN5ttALav9XP", -6.175, 106.8275),
    "bengaluru": ("discplace-G0tGUVYwl7T17Sb", 12.9789, 77.5917),
    "new-delhi": ("discplace-CzipmKodUYN2Dfx", 28.61, 77.23),
    "mumbai": ("discplace-Q5hkYsjZs1ZDJcU", 19.0761, 72.8775),
    "dubai": ("discplace-d3kg1aLIJ5ROF6S", 25.2048, 55.2708),
    "tel-aviv": ("discplace-fHkSoyCyugTZSbr", 32.08, 34.78),
    "auckland": ("discplace-NvBaYaVTkHmsPVy", -36.8406, 174.74),
    "brisbane": ("discplace-SQBjjDiskwFZwtG", -27.4678, 153.0281),
    "sydney": ("discplace-TPdKGPI56hGfOdi", -33.8678, 151.21),
    "melbourne": ("discplace-DlA8FnyHTxhIkN2", -37.8142, 144.9631),
    "lagos": ("discplace-ARF3ZNcu47bs56x", 6.455, 3.3841),
    "nairobi": ("discplace-YSx1DPerjjIyq7M", -1.2864, 36.8172),
    "capetown": ("discplace-YBoSEMjeIijj03X", -33.9221, 18.4231),
}

_FALLBACK_CATEGORIES: dict[str, str] = {
    "tech": "cat-tech",
    "food": "cat-fooddrink",
    "ai": "cat-ai",
    "arts": "cat-AzVAf6VmE9JEre4",
    "climate": "cat-climate",
    "fitness": "cat-0Km9ZnuBjFAjwFl",
    "wellness": "cat-C1VaNLnt25w9t6c",
    "crypto": "cat-crypto",
}

_FALLBACK_CONTINENTS: dict[str, str] = {
    **{s: "na" for s in [
        "atlanta", "austin", "boston", "calgary", "chicago", "dallas", "denver",
        "houston", "las-vegas", "la", "mexico-city", "miami", "minneapolis",
        "montreal", "nyc", "philadelphia", "phoenix", "portland", "salt-lake-city",
        "sd", "sf", "seattle", "toronto", "vancouver", "dc", "waterloo_ca",
    ]},
    **{s: "apac" for s in [
        "auckland", "bangkok", "bengaluru", "brisbane", "dubai",
        "ho-chi-minh-city", "hongkong", "honolulu", "jakarta", "kuala-lumpur",
        "manila", "melbourne", "mumbai", "new-delhi", "seoul", "singapore",
        "sydney", "taipei", "tel-aviv", "tokyo",
    ]},
    **{s: "sa" for s in [
        "bogota", "buenos-aires", "medellin", "rio", "saopaulo",
    ]},
    **{s: "europe" for s in [
        "amsterdam", "barcelona", "berlin", "brussels", "budapest",
        "copenhagen", "dublin", "geneva", "hamburg", "helsinki", "istanbul",
        "lausanne", "lisbon", "london", "madrid", "milan", "munich", "paris",
        "prague", "rome", "stockholm", "warsaw", "vienna", "zurich",
    ]},
    **{s: "africa" for s in ["lagos", "capetown", "nairobi"]},
}

_FALLBACK_PLACE_NAMES: dict[str, str] = {
    "sf": "San Francisco", "la": "Los Angeles", "las-vegas": "Las Vegas",
    "sd": "San Diego", "portland": "Portland", "salt-lake-city": "Salt Lake City",
    "phoenix": "Phoenix", "seattle": "Seattle", "vancouver": "Vancouver",
    "denver": "Denver", "calgary": "Calgary", "dallas": "Dallas",
    "austin": "Austin", "minneapolis": "Minneapolis", "houston": "Houston",
    "chicago": "Chicago", "mexico-city": "Mexico City", "atlanta": "Atlanta",
    "waterloo_ca": "Waterloo", "toronto": "Toronto", "honolulu": "Honolulu",
    "dc": "Washington DC", "philadelphia": "Philadelphia", "montreal": "Montreal",
    "nyc": "New York City", "miami": "Miami", "boston": "Boston",
    "medellin": "Medellín", "bogota": "Bogotá", "buenos-aires": "Buenos Aires",
    "saopaulo": "São Paulo", "rio": "Rio de Janeiro",
    "dublin": "Dublin", "london": "London", "stockholm": "Stockholm",
    "helsinki": "Helsinki", "amsterdam": "Amsterdam", "copenhagen": "Copenhagen",
    "brussels": "Brussels", "hamburg": "Hamburg", "paris": "Paris",
    "berlin": "Berlin", "lisbon": "Lisbon", "madrid": "Madrid",
    "lausanne": "Lausanne", "geneva": "Geneva", "zurich": "Zurich",
    "prague": "Prague", "warsaw": "Warsaw", "munich": "Munich",
    "barcelona": "Barcelona", "milan": "Milan", "vienna": "Vienna",
    "budapest": "Budapest", "rome": "Rome", "istanbul": "Istanbul",
    "tokyo": "Tokyo", "seoul": "Seoul", "taipei": "Taipei",
    "hongkong": "Hong Kong", "manila": "Manila",
    "ho-chi-minh-city": "Ho Chi Minh City", "bangkok": "Bangkok",
    "kuala-lumpur": "Kuala Lumpur", "singapore": "Singapore",
    "jakarta": "Jakarta", "bengaluru": "Bengaluru", "new-delhi": "New Delhi",
    "mumbai": "Mumbai", "dubai": "Dubai", "tel-aviv": "Tel Aviv",
    "auckland": "Auckland", "brisbane": "Brisbane", "sydney": "Sydney",
    "melbourne": "Melbourne", "lagos": "Lagos", "nairobi": "Nairobi",
    "capetown": "Cape Town",
}

_FALLBACK_CATEGORY_NAMES: dict[str, str] = {
    "tech": "Tech", "food": "Food & Drink", "ai": "AI",
    "arts": "Arts & Culture", "climate": "Climate", "fitness": "Fitness",
    "wellness": "Wellness", "crypto": "Crypto",
}



# ------------------------------------------------------------------
# Fetch from lu.ma/discover
# ------------------------------------------------------------------

_DiscoverData = tuple[
    dict[str, PlaceInfo],   # places
    dict[str, str],         # categories (slug → api_id)
    dict[str, str],         # continents (slug → continent code)
    dict[str, str],         # place_names (slug → display name)
    dict[str, str],         # category_names (slug → display name)
]


def _parse_discover_page(html: str) -> _DiscoverData:
    """Extract places, categories, continents, and display names from __NEXT_DATA__."""
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if not match:
        raise ValueError("__NEXT_DATA__ not found")

    data = json.loads(match.group(1))
    initial = data["props"]["pageProps"]["initialData"]

    places: dict[str, PlaceInfo] = {}
    place_names: dict[str, str] = {}
    for p in initial.get("places", []):
        place = p["place"]
        slug = place.get("slug")
        api_id = place.get("api_id")
        name = place.get("name")
        coord = place.get("coordinate", {})
        lat = coord.get("latitude")
        lon = coord.get("longitude")
        if slug and api_id and lat is not None and lon is not None:
            places[slug] = (api_id, float(lat), float(lon))
            if name:
                place_names[slug] = name

    categories: dict[str, str] = {}
    category_names: dict[str, str] = {}
    for c in initial.get("categories", []):
        cat = c["category"]
        slug = cat.get("slug")
        api_id = cat.get("api_id")
        name = cat.get("name")
        if slug and api_id:
            categories[slug] = api_id
            if name:
                category_names[slug] = name

    continents: dict[str, str] = {}
    for group in initial.get("places_by_continent", []):
        geo = group.get("geo_continent", "")
        for p in group.get("places", []):
            slug = p.get("place", {}).get("slug")
            if slug and geo:
                continents[slug] = geo

    if not places or not categories:
        raise ValueError(f"Incomplete data: {len(places)} places, {len(categories)} categories")

    return places, categories, continents, place_names, category_names


async def _fetch_discover_html() -> str:
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        resp = await client.get(
            "https://lu.ma/discover",
            headers={"accept": "text/html"},
        )
        resp.raise_for_status()
        return resp.text


# ------------------------------------------------------------------
# Serialization helpers
# ------------------------------------------------------------------

def _serialize_places(places: dict[str, PlaceInfo]) -> str:
    return json.dumps({slug: list(info) for slug, info in places.items()})


def _deserialize_places(raw: str) -> dict[str, PlaceInfo]:
    data = json.loads(raw)
    return {slug: (info[0], float(info[1]), float(info[2])) for slug, info in data.items()}


def _serialize_categories(cats: dict[str, str]) -> str:
    return json.dumps(cats)


def _deserialize_categories(raw: str) -> dict[str, str]:
    return json.loads(raw)


# ------------------------------------------------------------------
# Fuzzy matching
# ------------------------------------------------------------------

@dataclass
class MatchResult:
    exact: bool
    slug: Optional[str]
    candidates: list[str]  # formatted as "slug (Display Name)"


def _normalize(s: str) -> str:
    """Lowercase, strip, remove dots/commas, collapse whitespace/underscores to hyphens."""
    s = s.strip().lower()
    s = s.replace(".", "").replace(",", "")
    return re.sub(r"[\s_]+", "-", s)


def _fmt(slug: str, names: dict[str, str]) -> str:
    """Format a slug with its display name for user-facing messages."""
    name = names.get(slug)
    return f"{slug} ({name})" if name else slug


def _fuzzy_match(
    input_str: str,
    slugs: list[str],
    display_names: Optional[dict[str, str]] = None,
    aliases: Optional[dict[str, str]] = None,
) -> MatchResult:
    """Match a user string to the closest known slug.

    Matches against slugs, display names, and aliases (if provided).
    Returns exact=True when the input matches unambiguously.
    Otherwise returns up to 5 candidates with display names.
    """
    names = display_names or {}
    norm = _normalize(input_str)

    if norm in slugs:
        return MatchResult(exact=True, slug=norm, candidates=[])

    # Build a reverse lookup: normalized display name / alias → slug
    name_to_slug: dict[str, str] = {}
    for slug in slugs:
        name = names.get(slug)
        if name:
            name_to_slug[_normalize(name)] = slug
    if aliases:
        for alias, slug in aliases.items():
            if slug in slugs:
                name_to_slug[_normalize(alias)] = slug

    if norm in name_to_slug:
        return MatchResult(exact=True, slug=name_to_slug[norm], candidates=[])

    # Substring matches against both slugs and normalized display names
    substring_hits: list[str] = []
    seen: set[str] = set()
    for s in slugs:
        norm_name = _normalize(names[s]) if s in names else ""
        if norm in s or s in norm or (norm_name and (norm in norm_name or norm_name in norm)):
            if s not in seen:
                substring_hits.append(s)
                seen.add(s)

    if len(substring_hits) == 1:
        return MatchResult(exact=True, slug=substring_hits[0], candidates=[])

    # Edit-distance ranking against both slug and display name (take best)
    scored: list[tuple[int, str]] = []
    for s in slugs:
        d_slug = _edit_distance(norm, s)
        d_name = _edit_distance(norm, _normalize(names[s])) if s in names else d_slug
        scored.append((min(d_slug, d_name), s))
    scored.sort()

    combined = list(substring_hits)
    combined_set = set(substring_hits)
    for _d, s in scored:
        if s not in combined_set:
            combined.append(s)
            combined_set.add(s)
        if len(combined) >= 5:
            break

    best = combined[0] if combined else None
    return MatchResult(
        exact=False,
        slug=best,
        candidates=[_fmt(s, names) for s in combined[:5]],
    )


def _edit_distance(a: str, b: str) -> int:
    """Levenshtein distance between two strings."""
    if len(a) < len(b):
        return _edit_distance(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            cost = 0 if ca == cb else 1
            curr.append(min(curr[j] + 1, prev[j + 1] + 1, prev[j] + cost))
        prev = curr
    return prev[-1]


# ------------------------------------------------------------------
# Public interface
# ------------------------------------------------------------------

class LumaRegistry:
    """Provides up-to-date place and category mappings, cached in SQLite."""

    def __init__(self, store: EventStore) -> None:
        self._store = store
        self._places: Optional[dict[str, PlaceInfo]] = None
        self._categories: Optional[dict[str, str]] = None
        self._continents: Optional[dict[str, str]] = None
        self._place_names: Optional[dict[str, str]] = None
        self._category_names: Optional[dict[str, str]] = None

    def _load_cache(self) -> bool:
        """Try loading from SQLite cache. Returns True if cache is fresh."""
        p_row = self._store.get_setting(_SETTINGS_KEY_PLACES)
        c_row = self._store.get_setting(_SETTINGS_KEY_CATEGORIES)
        if not p_row or not c_row:
            return False

        p_val, p_updated = p_row
        c_val, c_updated = c_row
        now = datetime.now(tz=timezone.utc)

        try:
            self._places = _deserialize_places(p_val)
            self._categories = _deserialize_categories(c_val)
        except (json.JSONDecodeError, KeyError, IndexError):
            return False

        cont_row = self._store.get_setting(_SETTINGS_KEY_CONTINENTS)
        if cont_row:
            try:
                self._continents = json.loads(cont_row[0])
            except json.JSONDecodeError:
                pass

        pn_row = self._store.get_setting(_SETTINGS_KEY_PLACE_NAMES)
        if pn_row:
            try:
                self._place_names = json.loads(pn_row[0])
            except json.JSONDecodeError:
                pass

        cn_row = self._store.get_setting(_SETTINGS_KEY_CATEGORY_NAMES)
        if cn_row:
            try:
                self._category_names = json.loads(cn_row[0])
            except json.JSONDecodeError:
                pass

        oldest = min(p_updated, c_updated)
        return (now - oldest) < _CACHE_TTL

    def _save_cache(
        self,
        places: dict[str, PlaceInfo],
        categories: dict[str, str],
        continents: dict[str, str],
        place_names: dict[str, str],
        category_names: dict[str, str],
    ) -> None:
        self._store.set_setting(_SETTINGS_KEY_PLACES, _serialize_places(places))
        self._store.set_setting(_SETTINGS_KEY_CATEGORIES, _serialize_categories(categories))
        self._store.set_setting(_SETTINGS_KEY_CONTINENTS, json.dumps(continents))
        self._store.set_setting(_SETTINGS_KEY_PLACE_NAMES, json.dumps(place_names))
        self._store.set_setting(_SETTINGS_KEY_CATEGORY_NAMES, json.dumps(category_names))

    async def refresh(self) -> None:
        """Fetch fresh data from Luma and update the cache."""
        html = await _fetch_discover_html()
        places, categories, continents, place_names, category_names = _parse_discover_page(html)
        self._places = places
        self._categories = categories
        self._continents = continents
        self._place_names = place_names
        self._category_names = category_names
        self._save_cache(places, categories, continents, place_names, category_names)

    async def get_places(self) -> dict[str, PlaceInfo]:
        if self._places is None:
            fresh = self._load_cache()
            if not fresh:
                try:
                    await self.refresh()
                except Exception:
                    pass
        return self._places or _FALLBACK_PLACES

    async def get_categories(self) -> dict[str, str]:
        if self._categories is None:
            fresh = self._load_cache()
            if not fresh:
                try:
                    await self.refresh()
                except Exception:
                    pass
        return self._categories or _FALLBACK_CATEGORIES

    async def resolve_place(self, slug: str) -> Optional[str]:
        """Return the discover_place_api_id for a city slug, or None."""
        places = await self.get_places()
        info = places.get(slug)
        return info[0] if info else None

    async def resolve_category(self, slug: str) -> Optional[str]:
        """Return the discover_category_api_id for a category slug, or None."""
        cats = await self.get_categories()
        return cats.get(slug)

    async def city_slugs(self) -> list[str]:
        places = await self.get_places()
        return list(places.keys())

    async def category_slugs(self) -> list[str]:
        cats = await self.get_categories()
        return list(cats.keys())

    async def get_continents(self) -> dict[str, str]:
        if self._continents is None:
            await self.get_places()  # triggers _load_cache / refresh
        return self._continents or _FALLBACK_CONTINENTS

    async def get_place_names(self) -> dict[str, str]:
        if self._place_names is None:
            await self.get_places()
        return self._place_names or _FALLBACK_PLACE_NAMES

    async def get_category_names(self) -> dict[str, str]:
        if self._category_names is None:
            await self.get_categories()
        return self._category_names or _FALLBACK_CATEGORY_NAMES

    async def continent_of(self, city_slug: str) -> Optional[str]:
        """Return the continent code for a city slug (na, apac, sa, europe, africa)."""
        continents = await self.get_continents()
        return continents.get(city_slug)

    async def match_city(self, input_str: str) -> MatchResult:
        """Fuzzy-match a user-supplied city string to a known Luma slug."""
        places = await self.get_places()
        names = await self.get_place_names()
        return _fuzzy_match(input_str, list(places.keys()), names)

