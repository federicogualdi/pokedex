"""Test for pokemon translated rest api."""

import pytest
import respx

from httpx import AsyncClient
from httpx import Response

from pokedex.entrypoints.rest.schemas.shared import ErrorResponseSchema
from pokedex.settings import settings
from tests.integration.entrypoints.rest.data_generators_translation import TRANSLATED_FALLBACK_CASES
from tests.integration.entrypoints.rest.data_generators_translation import TRANSLATED_HAPPY_CASES


@pytest.mark.asyncio
@respx.mock
@pytest.mark.parametrize(("pokemon_name", "pokeapi_json", "translated_text", "expected_body"), TRANSLATED_HAPPY_CASES)
async def test_get_pokemon_translated_happy_path(
    client: AsyncClient,
    pokemon_name: str,
    pokeapi_json: dict,
    translated_text: str,
    expected_body: dict,
):
    """Happy path: description is translated and returned."""
    # Arrange
    poke_base = str(settings.pokeapi_base_url).rstrip("/")
    fun_base = str(settings.funtranslations_base_url).rstrip("/")
    fun_path = str(settings.funtranslations_shakespeare_path).lstrip("/")

    respx.get(f"{poke_base}/pokemon-species/{pokemon_name}").mock(
        return_value=Response(200, json=pokeapi_json),
    )
    respx.post(f"{fun_base}/{fun_path}").mock(
        return_value=Response(200, json={"contents": {"translated": translated_text}}),
    )

    # Act
    resp = await client.get(f"/api/pokemon/translated/{pokemon_name}")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == expected_body


@pytest.mark.asyncio
@respx.mock
@pytest.mark.parametrize(
    ("pokemon_name", "pokeapi_json", "upstream_status", "expected_body"),
    TRANSLATED_FALLBACK_CASES,
)
async def test_get_pokemon_translated_fallback_on_translation_error(
    client: AsyncClient,
    pokemon_name: str,
    pokeapi_json: dict,
    upstream_status: int,
    expected_body: dict,
):
    """Fallback path: if translation fails, endpoint still returns 200 with original description."""
    # Arrange
    poke_base = str(settings.pokeapi_base_url).rstrip("/")
    fun_base = str(settings.funtranslations_base_url).rstrip("/")
    fun_path = str(settings.funtranslations_shakespeare_path).lstrip("/")

    respx.get(f"{poke_base}/pokemon-species/{pokemon_name}").mock(
        return_value=Response(200, json=pokeapi_json),
    )
    respx.post(f"{fun_base}/{fun_path}").mock(
        return_value=Response(upstream_status, json={"detail": "x"}),
    )

    # Act
    resp = await client.get(f"/api/pokemon/translated/{pokemon_name}")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == expected_body


@pytest.mark.asyncio
@respx.mock
async def test_get_pokemon_translated_propagates_not_found(client: AsyncClient):
    """If species provider returns 404, endpoint returns 404."""
    # Arrange
    poke_base = str(settings.pokeapi_base_url).rstrip("/")
    respx.get(f"{poke_base}/pokemon-species/missing").mock(
        return_value=Response(404, json={"detail": "Not found"}),
    )

    # Act
    resp = await client.get("/api/pokemon/translated/missing")

    # Assert
    assert resp.status_code == 404
    err = ErrorResponseSchema(**resp.json())
    assert isinstance(err.details, str)
