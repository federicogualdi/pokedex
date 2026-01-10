"""State for pokemon cache."""

from dataclasses import dataclass

from pokedex.domains.pokemon.model import Pokemon
from pokedex.infrastructure.cache.keyed_locks import KeyedAsyncLocks
from pokedex.infrastructure.cache.memory_cache import InMemoryTTLCache
from pokedex.settings import Settings


@dataclass(frozen=True)
class CacheState:
    """Cache for pokemon state."""

    species_cache: InMemoryTTLCache[Pokemon]
    translation_cache: InMemoryTTLCache[str]
    locks: KeyedAsyncLocks


def build_cache_state(settings: Settings) -> CacheState:
    """Build cache state."""
    return CacheState(
        species_cache=InMemoryTTLCache(ttl_seconds=settings.cache_ttl_seconds, maxsize=settings.cache_maxsize),
        translation_cache=InMemoryTTLCache(ttl_seconds=settings.cache_ttl_seconds, maxsize=settings.cache_maxsize),
        locks=KeyedAsyncLocks(),
    )
