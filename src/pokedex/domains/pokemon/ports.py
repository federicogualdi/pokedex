"""Pokemon species info."""

from typing import Protocol

from pokedex.domains.pokemon.model import Pokemon


class PokemonSpeciesPort(Protocol):
    """Pokemon species info."""

    async def get_species_info(self, name: str) -> Pokemon:
        """Gets species info."""
        ...
