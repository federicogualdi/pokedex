"""Integration test for cache integration."""

import pytest
import respx

from httpx import AsyncClient
from httpx import Response

from pokedex.settings import settings
from tests.data.pokeapi_data_generators import flavor_en
from tests.data.pokeapi_data_generators import pokeapi_species_payload


@pytest.mark.asyncio
@respx.mock
async def test_cache_reduces_upstream_calls_for_translation(client: AsyncClient):
    """Ensure that cache is reduced upstream calls."""
    # Arrange
    name = "pikachu"
    poke_base = settings.pokeapi_base_url.rstrip("/")
    fun_base = settings.funtranslations_base_url.rstrip("/")

    # PokeAPI: always called once (species cached too if enabled)
    poke_route = respx.get(f"{poke_base}/pokemon-species/{name}").mock(
        return_value=Response(
            200,
            json=pokeapi_species_payload(
                name=name,
                habitat="forest",
                is_legendary=False,
                flavor_entries=[flavor_en("Original description.")],
            ),
        ),
    )

    # Funtranslations: should be called once across two endpoint hits
    fun_route = respx.post(f"{fun_base}/{settings.funtranslations_shakespeare_path.lstrip('/')}").mock(
        return_value=Response(
            200,
            json={"contents": {"translated": "Translated description.", "text": "x", "translation": "shakespeare"}},
        ),
    )

    # Act
    r1 = await client.get(f"/api/pokemon/translated/{name}")
    r2 = await client.get(f"/api/pokemon/translated/{name}")

    # Assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert poke_route.call_count == 1
    assert fun_route.call_count == 1


@pytest.mark.asyncio
@respx.mock
async def test_cache_reduces_upstream_calls_for_translation_multiple_call(client: AsyncClient):
    """Ensure that cache is reduced upstream calls."""
    # Arrange
    name = "pikachu"
    poke_base = settings.pokeapi_base_url.rstrip("/")
    fun_base = settings.funtranslations_base_url.rstrip("/")

    # PokeAPI: always called once (species cached too if enabled)
    poke_route = respx.get(f"{poke_base}/pokemon-species/{name}").mock(
        return_value=Response(
            200,
            json=pokeapi_species_payload(
                name=name,
                habitat="forest",
                is_legendary=False,
                flavor_entries=[flavor_en("Original description.")],
            ),
        ),
    )

    # Funtranslations: should be called once across two endpoint hits
    fun_route = respx.post(f"{fun_base}/{settings.funtranslations_shakespeare_path.lstrip('/')}").mock(
        return_value=Response(
            200,
            json={"contents": {"translated": "Translated description.", "text": "x", "translation": "shakespeare"}},
        ),
    )

    # Act
    r1 = await client.get(f"/api/pokemon/translated/{name}")
    r2 = await client.get(f"/api/pokemon/translated/{name}")
    r3 = await client.get(f"/api/pokemon/translated/{name}")
    r4 = await client.get(f"/api/pokemon/translated/{name}")

    # Assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 200
    assert r4.status_code == 200
    assert poke_route.call_count == 1
    assert fun_route.call_count == 1


@pytest.mark.asyncio
@respx.mock
async def test_cache_reduces_upstream_calls_for_translation_different_pokemon(client: AsyncClient):
    """Ensure that cache is reduced upstream calls."""
    # Arrange
    name = "pikachu"
    name2 = "mewtwo"
    poke_base = settings.pokeapi_base_url.rstrip("/")
    fun_base = settings.funtranslations_base_url.rstrip("/")

    # PokeAPI: always called once (species cached too if enabled)
    poke_route = respx.get(f"{poke_base}/pokemon-species/{name}").mock(
        return_value=Response(
            200,
            json=pokeapi_species_payload(
                name=name,
                habitat="forest",
                is_legendary=False,
                flavor_entries=[flavor_en("Original description.")],
            ),
        ),
    )
    poke_route2 = respx.get(f"{poke_base}/pokemon-species/{name2}").mock(
        return_value=Response(
            200,
            json=pokeapi_species_payload(
                name=name2,
                habitat="cave",
                is_legendary=True,
                flavor_entries=[flavor_en("Original description.")],
            ),
        ),
    )

    # Funtranslations: should be called once across two endpoint hits
    fun_route = respx.post(f"{fun_base}/{settings.funtranslations_shakespeare_path.lstrip('/')}").mock(
        return_value=Response(
            200,
            json={"contents": {"translated": "Translated shakespeare.", "text": "x", "translation": "shakespeare"}},
        ),
    )
    fun_route2 = respx.post(f"{fun_base}/{settings.funtranslations_yoda_path.lstrip('/')}").mock(
        return_value=Response(
            200,
            json={"contents": {"translated": "Translated yoda.", "text": "x", "translation": "yoda"}},
        ),
    )

    # Act
    r1 = await client.get(f"/api/pokemon/translated/{name}")
    r2 = await client.get(f"/api/pokemon/translated/{name}")

    assert poke_route.call_count == 1
    assert fun_route.call_count == 1

    r3 = await client.get(f"/api/pokemon/translated/{name2}")
    r4 = await client.get(f"/api/pokemon/translated/{name}")
    r5 = await client.get(f"/api/pokemon/translated/{name}")
    r6 = await client.get(f"/api/pokemon/translated/{name2}")

    # Assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 200
    assert r4.status_code == 200
    assert r5.status_code == 200
    assert r6.status_code == 200

    # 3rd party services called once
    assert poke_route.call_count == 1
    assert poke_route2.call_count == 1
    assert fun_route.call_count == 1
    assert fun_route2.call_count == 1

    # pokemon 1 consistency across the call
    assert r1.text == r2.text == r4.text == r5.text
    # pokemon 2 consistency across the call
    assert r3.text == r6.text
    # pokemon 1 is different from pokemon 2
    assert r1 != r3
