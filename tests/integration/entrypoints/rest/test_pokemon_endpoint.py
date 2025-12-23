"""Test for pokemon rest api."""

import pytest
import respx

from httpx import AsyncClient
from httpx import Response

from pokedex.entrypoints.rest.schemas.shared import ErrorResponseSchema
from pokedex.settings import settings
from tests.integration.entrypoints.rest.data_generators import CORNER_CASES
from tests.integration.entrypoints.rest.data_generators import ERROR_HTTP_CASES
from tests.integration.entrypoints.rest.data_generators import HAPPY_CASES


@pytest.mark.asyncio
@respx.mock
@pytest.mark.parametrize(("pokemon_name", "pokeapi_json", "expected_body"), HAPPY_CASES)
async def test_get_pokemon_happy_paths(client: AsyncClient, pokemon_name: str, pokeapi_json: dict, expected_body: dict):
    """Return 200 and the expected payload for valid Pokémon names."""
    # Arrange
    base = str(settings.pokeapi_base_url).rstrip("/")
    respx.get(f"{base}/pokemon-species/{pokemon_name}").mock(
        return_value=Response(200, json=pokeapi_json),
    )

    # Act
    resp = await client.get(f"/api/pokemon/{pokemon_name}")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == expected_body


@pytest.mark.asyncio
@respx.mock
@pytest.mark.parametrize(("pokemon_name", "pokeapi_json", "expected_body"), CORNER_CASES)
async def test_get_pokemon_corner_cases(
    client: AsyncClient,
    pokemon_name: str,
    pokeapi_json: dict,
    expected_body: dict,
):
    """Handle edge cases in successful upstream responses."""
    # Arrange
    base = str(settings.pokeapi_base_url).rstrip("/")
    respx.get(f"{base}/pokemon-species/{pokemon_name}").mock(
        return_value=Response(200, json=pokeapi_json),
    )

    # Act
    resp = await client.get(f"/api/pokemon/{pokemon_name}")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == expected_body


@pytest.mark.asyncio
@respx.mock
@pytest.mark.parametrize(("upstream_status", "api_expected_status"), ERROR_HTTP_CASES)
async def test_get_pokemon_error_mapping(client: AsyncClient, upstream_status: int, api_expected_status: int):
    """Map upstream HTTP errors to API error responses."""
    # Arrange
    base = str(settings.pokeapi_base_url).rstrip("/")
    respx.get(f"{base}/pokemon-species/missing").mock(
        return_value=Response(upstream_status, json={"detail": "x"}),
    )

    # Act
    resp = await client.get("/api/pokemon/missing")

    # Assert
    assert resp.status_code == api_expected_status
    body = resp.json()
    # Validate that the response matches our error contract
    err = ErrorResponseSchema(**body)
    assert isinstance(err, ErrorResponseSchema)
    assert isinstance(err.details, str)
