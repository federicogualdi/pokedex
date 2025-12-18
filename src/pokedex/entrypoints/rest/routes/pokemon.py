"""Pokemon Route Package."""

from fastapi import APIRouter
from fastapi import Depends
from starlette import status
from starlette.requests import Request

from pokedex.domains.pokemon.service import PokemonService
from pokedex.entrypoints.rest.schemas.pokemon import GetPokemonResponse
from pokedex.entrypoints.rest.schemas.shared import ErrorResponseSchema
from pokedex.infrastructure.http.clients.pokeapi.client import PokeApiClient
from pokedex.settings import settings

# router definition
router = APIRouter(prefix="/pokemon", tags=["Pokemon"])


def get_pokeapi_client(request: Request) -> PokeApiClient:
    """Get PokeAPI client."""
    return PokeApiClient(http=request.app.state.http, base_url=settings.pokeapi_base_url)


def pokemon_service_factory(request: Request) -> PokemonService:
    """Pokemon service factory."""
    return PokemonService(species_port=get_pokeapi_client(request))


@router.get(
    "/{name}",
    summary="Get Pokemon by name",
    response_model=GetPokemonResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Returns the Pokemon by name",
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema, "description": "Invalid input data"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema, "description": "Pokemon not found"},
    },
)
async def get_users_by_user_id(
    name: str,
    pokemon_service: PokemonService = Depends(pokemon_service_factory),
) -> GetPokemonResponse:
    """Get Pokemon by name."""
    pokemon = await pokemon_service.get_pokemon(name)
    return GetPokemonResponse(pokemon=pokemon)
