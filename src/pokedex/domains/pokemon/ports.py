"""Pokemon species info."""

from typing import Protocol

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.infrastructure.resilience.retry import RetryPolicy
from pokedex.infrastructure.resilience.retry import with_retry


class PokemonSpeciesPort(Protocol):
    """Pokemon species info."""

    async def get_species_info(self, name: str) -> Pokemon:
        """Gets species info."""
        ...


class TranslationPort(Protocol):
    """Translation port."""

    async def translate(self, text: str, strategy: TranslationStrategy) -> str:
        """Translate text with the given strategy."""
        ...


class RetryingPokemonSpeciesPort(PokemonSpeciesPort):
    """Retrying pokemon species info."""

    def __init__(self, inner: PokemonSpeciesPort, policy: RetryPolicy):
        """Initialize RetryingPokemonSpeciesPort."""
        self._inner = inner
        self._policy = policy

    async def get_species_info(self, name: str) -> Pokemon:
        """Gets species info."""
        return await with_retry(lambda: self._inner.get_species_info(name), self._policy)  # type: ignore[return-value]


class RetryingTranslationPort(TranslationPort):
    """Retrying translation."""

    def __init__(self, inner: TranslationPort, policy: RetryPolicy):
        """Init RetryingTranslationPort."""
        self._inner = inner
        self._policy = policy

    async def translate(self, text: str, strategy: TranslationStrategy) -> str:
        """Translate text with the given strategy and retry."""
        return await with_retry(lambda: self._inner.translate(text, strategy), self._policy)  # type: ignore[return-value]
