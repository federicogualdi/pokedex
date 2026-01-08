"""Pokemon species info."""

from typing import Protocol

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.translation_strategy import TranslationStrategy


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
