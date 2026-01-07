"""Pokeapi Http Client."""

from http import HTTPStatus
from typing import TypeVar

import httpx

from pokedex.domains.pokemon.exceptions import PokemonNotFoundError
from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.ports import PokemonSpeciesPort
from pokedex.infrastructure.http.base_http_client_adapter import BaseHttpClientAdapter
from pokedex.infrastructure.http.base_http_client_adapter import RequestSpec
from pokedex.infrastructure.http.clients.pokeapi.converters import to_domain_pokemon_info
from pokedex.infrastructure.http.clients.pokeapi.schemas import PokeApiSpeciesDTO
from pokedex.settings import get_logger

# logger
logger = get_logger()

T = TypeVar("T")


class PokeApiClient(BaseHttpClientAdapter, PokemonSpeciesPort):
    """Pokeapi Http Client."""

    client_name = "PokeApi"

    def __init__(self, http: httpx.AsyncClient, base_url: str):
        """Initializes PokeApiClient."""
        super().__init__(http, base_url)

    async def get_species_info(self, name: str) -> Pokemon:
        """Gets species info from Pokemon."""
        response = await self._request(
            method="GET",
            path=f"/pokemon-species/{name}",
        )
        dto = PokeApiSpeciesDTO.model_validate(response.json())
        logger.debug(f"Pokeapi response: {dto}")
        return to_domain_pokemon_info(dto)

    def _map_status(self, e: httpx.HTTPStatusError, spec: RequestSpec) -> Exception:
        status = e.response.status_code

        if status == HTTPStatus.NOT_FOUND:
            return PokemonNotFoundError(spec.path.split("/")[-1])

        return super()._map_status(e, spec)
