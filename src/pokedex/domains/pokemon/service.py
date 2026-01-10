"""Pokemon service module."""

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.ports import PokemonSpeciesPort
from pokedex.domains.pokemon.ports import TranslationPort
from pokedex.domains.pokemon.translation_strategy import TranslationStrategyPolicy
from pokedex.settings import get_logger
from pokedex.shared.exceptions import ExecutionError

logger = get_logger()


class PokemonService:
    """Pokemon service."""

    def __init__(
        self,
        species_port: PokemonSpeciesPort,
        translation_port: TranslationPort,
        strategy_policy: TranslationStrategyPolicy | None = None,
    ):
        """Pokemon service init."""
        self._species_port = species_port
        self._translation_port = translation_port
        self._strategy_policy = strategy_policy or TranslationStrategyPolicy()

    async def get_pokemon(self, name: str) -> Pokemon:
        """Get a Pokemon by name."""
        return await self._species_port.get_species_info(name)

    async def get_pokemon_with_translated_description(self, name: str) -> Pokemon:
        """Get a Pokemon by name with translated description."""
        pokemon = await self._species_port.get_species_info(name)
        strategy = self._strategy_policy.choose(pokemon)

        try:
            translated = await self._translation_port.translate(pokemon.description, strategy)
            pokemon = pokemon.model_copy(update={"description": translated})
        except ExecutionError:
            logger.exception(
                f"Error while translating {pokemon.name} description with {strategy}. Fallback with the default one.",
            )
        return pokemon
