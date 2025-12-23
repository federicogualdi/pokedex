"""Helper file to build pokeapi datas."""

from pokedex.infrastructure.http.clients.pokeapi.schemas import FlavorTextEntryDTO
from pokedex.infrastructure.http.clients.pokeapi.schemas import HabitatDTO
from pokedex.infrastructure.http.clients.pokeapi.schemas import LangDTO
from pokedex.infrastructure.http.clients.pokeapi.schemas import PokeApiSpeciesDTO


def flavor_entry(lang: str, text: str) -> FlavorTextEntryDTO:
    """Build a PokeAPI flavor text entry for the given language."""
    return FlavorTextEntryDTO(
        flavor_text=text,
        language=LangDTO(name=lang),
    )


def flavor_en(text: str) -> FlavorTextEntryDTO:
    """Build an English PokeAPI flavor text entry."""
    return flavor_entry("en", text)


def flavor_it(text: str) -> FlavorTextEntryDTO:
    """Build an Italian PokeAPI flavor text entry."""
    return flavor_entry("it", text)


def pokeapi_species_payload(
    *,
    name: str,
    habitat: str | None = None,
    is_legendary: bool = False,
    flavor_entries: list[FlavorTextEntryDTO] | None = None,
) -> dict:
    """Build a PokeAPI Pokémon species payload for tests."""
    return PokeApiSpeciesDTO(
        name=name,
        habitat=HabitatDTO(name=habitat) if habitat is not None else None,
        is_legendary=is_legendary,
        flavor_text_entries=flavor_entries or [],
    ).model_dump()
