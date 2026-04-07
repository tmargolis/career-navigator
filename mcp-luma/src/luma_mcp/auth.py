"""Browser-based Luma login and session validation."""

from __future__ import annotations

from typing import Optional

import httpx

_LOGIN_URL = "https://lu.ma/signin"
_COOKIE_NAME = "luma.auth-session-key"
_VALIDATE_URL = "https://api.lu.ma/home/get-subscribed-calendars"
_LOGIN_TIMEOUT_S = 120
_POLL_INTERVAL_S = 1


def browser_login() -> str:
    """Open a browser to lu.ma/signin, wait for the user to log in, return the session cookie.

    Raises ImportError if Playwright is not installed.
    Raises TimeoutError if the user doesn't complete login within 2 minutes.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise ImportError(
            "Playwright is required for browser login. Run these in a normal "
            "terminal (not Cursor's built-in terminal, which may sandbox the install):\n"
            "  cd /path/to/Luma\\ Cal\\ MCP\n"
            "  uv pip install -e '.[auth]'\n"
            "  playwright install chromium"
        )

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(_LOGIN_URL)

        elapsed = 0.0
        cookie_value: Optional[str] = None
        while elapsed < _LOGIN_TIMEOUT_S:
            for cookie in context.cookies():
                if cookie["name"] == _COOKIE_NAME and cookie["value"]:
                    cookie_value = cookie["value"]
                    break
            if cookie_value:
                break
            page.wait_for_timeout(int(_POLL_INTERVAL_S * 1000))
            elapsed += _POLL_INTERVAL_S

        browser.close()

    if not cookie_value:
        raise TimeoutError(
            f"Login not completed within {_LOGIN_TIMEOUT_S}s. Please try again."
        )
    return cookie_value


async def validate_session(cookie: str) -> bool:
    """Check whether a Luma session cookie is still valid.

    Returns True if the cookie authenticates successfully, False otherwise.
    """
    headers = {
        "accept": "application/json",
        "cookie": f"{_COOKIE_NAME}={cookie}" if "=" not in cookie else cookie,
        "origin": "https://lu.ma",
        "referer": "https://lu.ma/",
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(_VALIDATE_URL, headers=headers)
            return resp.status_code == 200
        except httpx.HTTPError:
            return False
