"""Test for pokeapi rest client service."""

import json

import httpx
import pytest

from httpx import MockTransport
from httpx import Request
from httpx import Response

from pokedex.domains.pokemon.exceptions import PokemonNotFoundError
from pokedex.infrastructure.http.clients.pokeapi.client import PokeApiClient
from pokedex.shared.exceptions import ExecutionError
from tests.data.pokeapi_data_generators import flavor_en
from tests.data.pokeapi_data_generators import flavor_it
from tests.data.pokeapi_data_generators import pokeapi_species_payload

BASE = "https://pokeapi.co/api/v2"


def transport_json(status_code: int, payload: dict) -> MockTransport:
    """Transport encoding."""

    def handler(request: Request) -> Response:
        content = json.dumps(payload).encode("utf-8")
        return Response(status_code=status_code, content=content, request=request)

    return MockTransport(handler)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("payload", "expected_name", "expected_description", "expected_habitat", "expected_legendary"),
    [
        (
            pokeapi_species_payload(
                name="mewtwo",
                habitat="cave",
                is_legendary=True,
                flavor_entries=[flavor_it("ciao"), flavor_en("A test\ntext.\f")],
            ),
            "mewtwo",
            "A test text.",
            "cave",
            True,
        ),
        (
            pokeapi_species_payload(
                name="pikachu",
                habitat="forest",
                is_legendary=False,
                flavor_entries=[flavor_it("solo italiano")],
            ),
            "pikachu",
            "solo italiano",
            "forest",
            False,
        ),
        (
            pokeapi_species_payload(
                name="bulbasaur",
                habitat=None,
                is_legendary=False,
                flavor_entries=[flavor_en("Hello")],
            ),
            "bulbasaur",
            "Hello",
            None,
            False,
        ),
    ],
)
async def test_pokeapi_client_parses_species(
    payload: dict,
    expected_name: str,
    expected_description: str,
    expected_habitat: str,
    expected_legendary: bool,
):
    """Test pokeapi client parsing."""
    # Arrange
    transport = transport_json(200, payload)
    async with httpx.AsyncClient(transport=transport, base_url=BASE) as http:
        client = PokeApiClient(http=http, base_url=BASE)

        # Act
        info = await client.get_species_info(payload.get("name"))
        assert info.name == expected_name
        assert info.description == expected_description

    # Assert
    assert info.name == expected_name
    assert info.description == expected_description
    assert info.habitat == expected_habitat
    assert info.is_legendary is expected_legendary


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status_code", "expected_exc"),
    [
        (404, PokemonNotFoundError),
        (500, ExecutionError),
        (503, ExecutionError),
    ],
)
async def test_pokeapi_client_maps_http_errors(status_code: int, expected_exc: Exception):
    """Test pokeapi client errors."""
    # Arrange
    transport = transport_json(status_code, {"detail": "x"})
    async with httpx.AsyncClient(transport=transport, base_url=BASE) as http:
        client = PokeApiClient(http=http, base_url=BASE)

        # Act / Assert
        with pytest.raises(expected_exc):
            await client.get_species_info("missing")


@pytest.mark.asyncio
async def test_pokeapi_client_maps_network_errors_to_upstream():
    """Test pokeapi client error upstream."""

    # Arrange
    def handler(_: Request) -> Response:
        raise httpx.ConnectError(
            "boom",
            request=Request("GET", f"{BASE}/pokemon-species/x"),
        )

    transport = MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url=BASE) as http:
        client = PokeApiClient(http=http, base_url=BASE)

        # Act / Assert
        with pytest.raises(ExecutionError):
            await client.get_species_info("mewtwo")
