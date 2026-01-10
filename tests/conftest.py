"""Pytest fixtures for testing."""

import httpx
import pytest_asyncio

from pokedex.domains.pokemon.ports import TranslationPort
from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.entrypoints.rest.server import app
from pokedex.infrastructure.cache.state import build_cache_state
from pokedex.settings import settings


@pytest_asyncio.fixture
async def client():
    """Http Client for testing."""
    app.state.http = httpx.AsyncClient()
    app.state.cache = build_cache_state(settings)
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class NoOpTranslationPort(TranslationPort):
    """No-op translator for testing."""

    async def translate(self, text: str, strategy: TranslationStrategy) -> str:
        """Fake translate text."""
        return text
