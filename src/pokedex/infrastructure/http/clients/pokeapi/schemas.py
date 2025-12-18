"""Pokeapi http client schemas."""

from pydantic import BaseModel
from pydantic import Field


class LangDTO(BaseModel):
    """Pokeapi flavor language."""

    name: str = Field()


class FlavorTextEntryDTO(BaseModel):
    """Pokeapi flavor text entry."""

    flavor_text: str
    language: LangDTO


class HabitatDTO(BaseModel):
    """Pokemon habitat."""

    name: str


class PokeApiSpeciesDTO(BaseModel):
    """Pokeapi species."""

    name: str
    habitat: HabitatDTO | None = None
    is_legendary: bool = False
    flavor_text_entries: list[FlavorTextEntryDTO] = []
