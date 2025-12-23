"""Http Client."""

import httpx

from pokedex.settings import Settings


def build_async_http_client(settings: Settings) -> httpx.AsyncClient:
    """Build a httpx client."""
    timeout = httpx.Timeout(settings.http_timeout_seconds)
    return httpx.AsyncClient(timeout=timeout)
