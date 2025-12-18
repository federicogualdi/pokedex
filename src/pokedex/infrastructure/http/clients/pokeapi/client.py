"""Pokeapi Http Client."""

from http import HTTPStatus

import httpx

from pokedex.domains.pokemon.exceptions import PokemonNotFoundError
from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.ports import PokemonSpeciesPort
from pokedex.infrastructure.http.clients.pokeapi.converters import to_domain_pokemon_info
from pokedex.infrastructure.http.clients.pokeapi.schemas import PokeApiSpeciesDTO
from pokedex.settings import get_logger
from pokedex.shared.exceptions import ExecutionError

# logger
logger = get_logger()


class PokeApiClient(PokemonSpeciesPort):
    """Pokeapi Http Client."""

    def __init__(self, http: httpx.AsyncClient, base_url: str):
        """Initializes PokeApiClient."""
        self._http = http
        self._base = base_url.rstrip("/")

    async def get_species_info(self, name: str) -> Pokemon:
        """Gets species info from Pokemon."""
        url = f"{self._base}/pokemon-species/{name}"

        try:
            r = await self._http.get(url)
        except httpx.TimeoutException as e:
            raise ExecutionError("PokeAPI timeout") from e
        except httpx.RequestError as e:
            raise ExecutionError("PokeAPI request failed") from e

        if r.status_code == HTTPStatus.NOT_FOUND:
            raise PokemonNotFoundError(name)
        if r.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            raise ExecutionError("PokeAPI error")

        r.raise_for_status()

        dto = PokeApiSpeciesDTO.model_validate(r.json())
        return to_domain_pokemon_info(dto)
