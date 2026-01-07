"""Test for pokemon service."""

from unittest.mock import AsyncMock

import pytest

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.ports import PokemonSpeciesPort
from pokedex.domains.pokemon.service import PokemonService
from pokedex.shared.exceptions import NotFoundError  # se si chiama shared/errors.py -> cambia import
from tests.conftest import NoOpTranslationPort


class FakeSpeciesPort(PokemonSpeciesPort):
    """Fake SpeciesPort Class."""

    async def get_species_info(self, name: str) -> Pokemon:
        """Fake get_species_info method."""
        return Pokemon(
            name=name.lower(),
            description="fake-description",
            habitat="forest",
            isLegendary=False,
        )


@pytest.mark.asyncio
async def test_get_pokemon_returns_species_from_port():
    """Ensure PokemonService retrieves species data through the SpeciesPort and returns the expected domain object."""
    # Arrange
    svc = PokemonService(species_port=FakeSpeciesPort(), translation_port=NoOpTranslationPort)

    # Act
    result = await svc.get_pokemon("MewTwo")

    # Assert
    assert result.name == "mewtwo"
    assert result.description == "fake-description"


@pytest.mark.asyncio
async def test_get_pokemon_calls_species_port_once():
    """Ensure PokemonService calls the SpeciesPort exactly once when retrieving a Pokemon."""
    # Arrange
    port = AsyncMock()
    port.get_species_info.return_value = Pokemon(
        name="mewtwo",
        description="desc",
        habitat="cave",
        isLegendary=True,
    )
    svc = PokemonService(species_port=port, translation_port=NoOpTranslationPort)

    # Act
    name = "mewtwo"
    out = await svc.get_pokemon(name)

    # Assert
    port.get_species_info.assert_awaited_once()
    assert out.name == "mewtwo"
    assert out.is_legendary is True


@pytest.mark.asyncio
async def test_get_pokemon_propagates_not_found():
    """Test get missing pokemon returns not found."""
    # Arrange
    port = AsyncMock()
    port.get_species_info.side_effect = NotFoundError("Pokemon 'missing' not found")
    svc = PokemonService(species_port=port, translation_port=NoOpTranslationPort)

    # Act / Assert
    with pytest.raises(NotFoundError):
        await svc.get_pokemon("missing")
