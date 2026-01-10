"""Test cache decorators."""

from unittest.mock import AsyncMock

import pytest

from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.infrastructure.cache.decorators import CachedTranslationPort
from pokedex.infrastructure.cache.keyed_locks import KeyedAsyncLocks
from pokedex.infrastructure.cache.memory_cache import InMemoryTTLCache


@pytest.mark.asyncio
async def test_cached_translation_port_miss_then_hit_calls_inner_once():
    """Tests that the cache is inner once."""
    # Arrange
    inner = AsyncMock()
    inner.translate.return_value = "Translated"

    cache = InMemoryTTLCache(ttl_seconds=60, maxsize=10)
    locks = KeyedAsyncLocks()
    cached = CachedTranslationPort(inner, cache=cache, locks=locks)

    # Act
    a = await cached.translate("Hello", TranslationStrategy.SHAKESPEARE)
    b = await cached.translate("Hello", TranslationStrategy.SHAKESPEARE)

    # Assert
    assert a == "Translated"
    assert b == "Translated"
    inner.translate.assert_awaited_once_with("Hello", TranslationStrategy.SHAKESPEARE)
