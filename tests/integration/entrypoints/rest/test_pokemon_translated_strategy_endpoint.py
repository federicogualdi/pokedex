"""Rest tests for pokemon translated strategy endpoint."""

import pytest
import respx

from _pytest.monkeypatch import MonkeyPatch
from httpx import AsyncClient
from httpx import Response

from pokedex.settings import settings
from tests.data.pokeapi_data_generators import flavor_en
from tests.data.pokeapi_data_generators import pokeapi_species_payload


@pytest.mark.asyncio
@respx.mock
async def test_translated_endpoint_shakespeare_happy_path(client: AsyncClient, monkeypatch: MonkeyPatch):
    """Test shakespeare-happy-path."""
    # Arrange
    monkeypatch.setattr(settings, "funtranslations_shakespeare_path", "shakespeare")

    poke_base = str(settings.pokeapi_base_url).rstrip("/")
    fun_base = str(settings.funtranslations_base_url).rstrip("/")

    respx.get(f"{poke_base}/pokemon-species/pikachu").mock(
        return_value=Response(
            200,
            json=pokeapi_species_payload(
                name="pikachu",
                habitat="forest",
                is_legendary=False,
                flavor_entries=[flavor_en("Original")],
            ),
        ),
    )

    respx.post(f"{fun_base}/shakespeare").mock(
        return_value=Response(
            200,
            json={"contents": {"translated": "Translated", "text": "x", "translation": "shakespeare"}},
        ),
    )

    # Act
    resp = await client.get("/api/pokemon/translated/pikachu")

    # Assert
    assert resp.status_code == 200
    assert resp.json()["pokemon"]["description"] == "Translated"


@pytest.mark.asyncio
@respx.mock
async def test_translated_endpoint_yoda_selected_but_fallbacks(client: AsyncClient):
    """Test yoda-selected-but-fallbacks."""
    # Arrange
    poke_base = str(settings.pokeapi_base_url).rstrip("/")

    respx.get(f"{poke_base}/pokemon-species/mewtwo").mock(
        return_value=Response(
            200,
            json=pokeapi_species_payload(
                name="mewtwo",
                habitat="cave",
                is_legendary=True,
                flavor_entries=[flavor_en("Original")],
            ),
        ),
    )

    # No respx mock for funtranslations: client raises before making HTTP (strategy not supported yet)

    # Act
    resp = await client.get("/api/pokemon/translated/mewtwo")

    # Assert
    assert resp.status_code == 200
    assert resp.json()["pokemon"]["description"] == "Original"
