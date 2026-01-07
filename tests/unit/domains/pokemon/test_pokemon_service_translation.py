"""Tests for PokemonService translation feature."""

from unittest.mock import AsyncMock

import pytest

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.service import PokemonService
from pokedex.shared.exceptions import ExecutionError


@pytest.mark.asyncio
async def test_get_pokemon_with_translated_description_happy_path():
    """When translation works, the returned pokemon has translated description."""
    # Arrange
    species_port = AsyncMock()
    translation_port = AsyncMock()

    species_port.get_species_info.return_value = Pokemon(
        name="mewtwo",
        description="Original",
        habitat="rare",
        isLegendary=True,
    )
    translation_port.shakespeare_translation.return_value = "Translated"

    svc = PokemonService(species_port=species_port, translation_port=translation_port)

    # Act
    out = await svc.get_pokemon_with_translated_description("mewtwo")

    # Assert
    species_port.get_species_info.assert_awaited_once_with("mewtwo")
    translation_port.shakespeare_translation.assert_awaited_once_with("Original")
    assert out.description == "Translated"


@pytest.mark.asyncio
async def test_get_pokemon_with_translated_description_fallback_on_execution_error():
    """When translation fails, we fallback to the original description."""
    # Arrange
    species_port = AsyncMock()
    translation_port = AsyncMock()

    species_port.get_species_info.return_value = Pokemon(
        name="pikachu",
        description="Original",
        habitat="forest",
        isLegendary=False,
    )
    translation_port.shakespeare_translation.side_effect = ExecutionError("rate limit")

    svc = PokemonService(species_port=species_port, translation_port=translation_port)

    # Act
    out = await svc.get_pokemon_with_translated_description("pikachu")

    # Assert
    species_port.get_species_info.assert_awaited_once_with("pikachu")
    translation_port.shakespeare_translation.assert_awaited_once_with("Original")
    assert out.description == "Original"
