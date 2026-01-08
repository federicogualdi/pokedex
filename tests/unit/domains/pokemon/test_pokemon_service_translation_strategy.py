"""Test for service that uses strategy policy."""

from unittest.mock import AsyncMock

import pytest

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.service import PokemonService
from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.domains.pokemon.translation_strategy import TranslationStrategyPolicy


class FixedPolicy(TranslationStrategyPolicy):
    """Fixed policy for testing."""

    def __init__(self, strategy: TranslationStrategy):
        """Initialize."""
        self._strategy = strategy

    def choose(self, pokemon: Pokemon) -> TranslationStrategy:
        """Choose a pokemon from this strategy."""
        return self._strategy


@pytest.mark.asyncio
async def test_service_translates_with_shakespeare_when_policy_says_so():
    """Test service translates with shakespeare."""
    # Arrange
    species_port = AsyncMock()
    translation_port = AsyncMock()

    species_port.get_species_info.return_value = Pokemon(
        name="pikachu",
        description="Original",
        habitat="forest",
        isLegendary=False,
    )
    translation_port.translate.return_value = "Translated"

    svc = PokemonService(
        species_port=species_port,
        translation_port=translation_port,
        strategy_policy=FixedPolicy(TranslationStrategy.SHAKESPEARE),
    )

    # Act
    out = await svc.get_pokemon_with_translated_description("pikachu")

    # Assert
    translation_port.translate.assert_awaited_once_with("Original", TranslationStrategy.SHAKESPEARE)
    assert out.description == "Translated"


@pytest.mark.asyncio
async def test_service_translates_with_yoda_when_policy_says_so():
    """Test service translates with yoda."""
    # Arrange
    species_port = AsyncMock()
    translation_port = AsyncMock()

    species_port.get_species_info.return_value = Pokemon(
        name="mewtwo",
        description="Original",
        habitat="cave",
        isLegendary=True,
    )
    translation_port.translate.return_value = "Translated"

    svc = PokemonService(
        species_port=species_port,
        translation_port=translation_port,
        strategy_policy=FixedPolicy(TranslationStrategy.YODA),
    )

    # Act
    out = await svc.get_pokemon_with_translated_description("mewtwo")

    # Assert
    translation_port.translate.assert_awaited_once_with("Original", TranslationStrategy.YODA)
    assert out.description == "Translated"
