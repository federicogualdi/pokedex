"""Pokemon Route Package."""

from fastapi import APIRouter
from fastapi import Depends
from starlette import status
from starlette.requests import Request

from pokedex.domains.pokemon.ports import PokemonSpeciesPort
from pokedex.domains.pokemon.ports import RetryingPokemonSpeciesPort
from pokedex.domains.pokemon.ports import RetryingTranslationPort
from pokedex.domains.pokemon.ports import TranslationPort
from pokedex.domains.pokemon.service import PokemonService
from pokedex.domains.pokemon.translation_strategy import TranslationStrategyPolicy
from pokedex.entrypoints.rest.schemas.pokemon import GetPokemonResponse
from pokedex.entrypoints.rest.schemas.shared import ErrorResponseSchema
from pokedex.infrastructure.cache.decorators import CachedPokemonSpeciesPort
from pokedex.infrastructure.cache.decorators import CachedTranslationPort
from pokedex.infrastructure.http.clients.funtranslations.client import FuntranslationsApiClient
from pokedex.infrastructure.http.clients.funtranslations.client import FunTranslator
from pokedex.infrastructure.http.clients.funtranslations.client import ShakespeareTranslator
from pokedex.infrastructure.http.clients.funtranslations.client import YodaTranslator
from pokedex.infrastructure.http.clients.pokeapi.client import PokeApiClient
from pokedex.infrastructure.resilience.retry import RetryPolicy
from pokedex.settings import settings

# router definition
router = APIRouter(prefix="/pokemon", tags=["Pokemon"])


def get_available_translator() -> list[FunTranslator]:
    """Get available translator."""
    return [ShakespeareTranslator(), YodaTranslator()]


def get_pokemon_species_client(request: Request) -> PokemonSpeciesPort:
    """Get Pokemon Species client."""
    raw = PokeApiClient(
        http=request.app.state.http,
        base_url=settings.pokeapi_base_url,
    )

    # Retry layer (optional)
    if settings.retry.enabled:
        client: PokemonSpeciesPort = RetryingPokemonSpeciesPort(
            raw,
            policy=RetryPolicy(attempts=settings.retry.attempts),
        )
    else:
        client = raw

    # Cache layer (optional)
    if not settings.cache.enabled:
        return client

    cache_state = request.app.state.cache
    return CachedPokemonSpeciesPort(
        client,
        cache=cache_state.species_cache,
        locks=cache_state.locks,
    )


def get_translation_client(request: Request) -> TranslationPort:
    """Get Translation client."""
    raw = FuntranslationsApiClient(
        http=request.app.state.http,
        base_url=settings.funtranslations_base_url,
        translators=get_available_translator(),
    )

    # Retry layer (optional)
    if settings.retry.enabled:
        client: TranslationPort = RetryingTranslationPort(
            raw,
            policy=RetryPolicy(attempts=settings.retry.attempts),
        )
    else:
        client = raw

    # Cache layer (optional)
    if not settings.cache.enabled:
        return client

    cache_state = request.app.state.cache
    return CachedTranslationPort(
        client,
        cache=cache_state.translation_cache,
        locks=cache_state.locks,
    )


def pokemon_service_factory(request: Request) -> PokemonService:
    """Pokemon service factory."""
    return PokemonService(
        species_port=get_pokemon_species_client(request),
        translation_port=get_translation_client(request),
        strategy_policy=TranslationStrategyPolicy(),
    )


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
async def get_pokemon_by_name(
    name: str,
    pokemon_service: PokemonService = Depends(pokemon_service_factory),
) -> GetPokemonResponse:
    """Get Pokemon by name."""
    pokemon = await pokemon_service.get_pokemon(name)
    return GetPokemonResponse(pokemon=pokemon)


@router.get(
    "/translated/{name}",
    summary="Get Pokemon by name with translated description",
    response_model=GetPokemonResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Returns the Pokemon by name with translated description",
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema, "description": "Invalid input data"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema, "description": "Pokemon not found"},
    },
)
async def get_pokemon_by_name_with_translated_description(
    name: str,
    pokemon_service: PokemonService = Depends(pokemon_service_factory),
) -> GetPokemonResponse:
    """Get Pokemon by name with translated description."""
    pokemon = await pokemon_service.get_pokemon_with_translated_description(name)
    return GetPokemonResponse(pokemon=pokemon)
