"""Decorators."""

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.ports import PokemonSpeciesPort
from pokedex.domains.pokemon.ports import TranslationPort
from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.infrastructure.cache.keyed_locks import KeyedAsyncLocks
from pokedex.infrastructure.cache.keys import pokemon_species_key
from pokedex.infrastructure.cache.keys import translation_key
from pokedex.infrastructure.cache.memory_cache import InMemoryTTLCache


class CachedPokemonSpeciesPort(PokemonSpeciesPort):
    """Decorator that adds cache to a PokemonSpeciesPort."""

    def __init__(self, inner: PokemonSpeciesPort, cache: InMemoryTTLCache[Pokemon], locks: KeyedAsyncLocks):
        """Initialize the cache."""
        self._inner = inner
        self._cache = cache
        self._locks = locks

    async def get_species_info(self, name: str) -> Pokemon:
        """Get Pokemon Species from cache. If miss, query it and update cache."""
        key = pokemon_species_key(name)

        cached = self._cache.get(key)
        if cached is not None:
            return cached

        lock = await self._locks.lock_for(key)
        async with lock:
            cached2 = self._cache.get(key)
            if cached2 is not None:
                return cached2

            value = await self._inner.get_species_info(name)
            self._cache.set(key, value)
            return value


class CachedTranslationPort(TranslationPort):
    """Decorator that adds cache to TranslationPort (Shakespeare only in current version)."""

    def __init__(self, inner: TranslationPort, cache: InMemoryTTLCache[str], locks: KeyedAsyncLocks):
        """Initialize the cache."""
        self._inner = inner
        self._cache = cache
        self._locks = locks

    async def translate(self, text: str, strategy: TranslationStrategy) -> str:
        """Get Translation from cache. If miss, query it and update cache."""
        key = translation_key(text, strategy)

        cached = self._cache.get(key)
        if cached is not None:
            return cached

        lock = await self._locks.lock_for(key)
        async with lock:
            cached2 = self._cache.get(key)
            if cached2 is not None:
                return cached2

            value = await self._inner.translate(text, strategy)
            self._cache.set(key, value)
            return value
