"""Pokemon service module."""

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.ports import PokemonSpeciesPort
from pokedex.domains.pokemon.ports import TranslationPort
from pokedex.settings import get_logger
from pokedex.shared.exceptions import ExecutionError

logger = get_logger()


class PokemonService:
    """Pokemon service."""

    def __init__(self, species_port: PokemonSpeciesPort, translation_port: TranslationPort):
        """Pokemon service init."""
        self._species_port = species_port
        self._translation_port = translation_port

    async def get_pokemon(self, name: str) -> Pokemon:
        """Get a Pokemon by name."""
        return await self._species_port.get_species_info(name)

    async def get_pokemon_with_translated_description(self, name: str) -> Pokemon:
        """Get a Pokemon by name with translated description."""
        pokemon = await self._species_port.get_species_info(name)
        try:
            pokemon.description = await self._translation_port.shakespeare_translation(pokemon.description)
        except ExecutionError:
            logger.exception(
                f"Error while translating {pokemon.name} description with shakespeare. Fallback with the default one.",
            )
        return pokemon
