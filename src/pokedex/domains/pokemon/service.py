"""Pokemon service module."""

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.ports import PokemonSpeciesPort
from pokedex.settings import get_logger

logger = get_logger()


class PokemonService:
    """Pokemon service."""

    def __init__(self, species_port: PokemonSpeciesPort):
        """Pokemon service init."""
        self._species_port = species_port

    async def get_pokemon(self, name: str) -> Pokemon:
        """Get a Pokemon by name."""
        return await self._species_port.get_species_info(name)
