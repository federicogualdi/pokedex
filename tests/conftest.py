"""Pytest fixtures for testing."""

import httpx
import pytest_asyncio

from pokedex.domains.pokemon.ports import TranslationPort
from pokedex.entrypoints.rest.server import app


@pytest_asyncio.fixture
async def client():
    """Http Client for testing."""
    app.state.http = httpx.AsyncClient()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class NoOpTranslationPort(TranslationPort):
    """No-op translator for testing."""

    async def shakespeare_translation(self, text: str) -> str:
        """Fake translate text."""
        return text
