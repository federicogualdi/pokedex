"""Pokeapi to domain model converters."""

from pokedex.domains.pokemon.model import Pokemon
from pokedex.infrastructure.http.clients.pokeapi.schemas import PokeApiSpeciesDTO
from pokedex.settings import settings


def normalize_flavor_text(flavor_text: str) -> str:
    r"""Normalize Pokémon species flavor text.

    This function cleans and normalizes flavor text coming from Pokedex datasets where early game text formatting is
    preserved using special characters.

    Normalization rules applied:
        - Form feed characters ('\\f') are treated as page breaks and converted to newlines.
        - Soft hyphens (U+00AD) used for hard hyphenation are removed.
        - Soft hyphen followed by newline ('\\u00ad\\n') is removed entirely
          to rejoin split words.
        - Hyphen + newline ('-\\n') is preserved as a real hyphen.
        - All remaining newlines are replaced with spaces.
        - Consecutive whitespace is collapsed into a single space.

    These rules follow the recommendations discussed in:
    https://github.com/veekun/pokedex/issues/218#issuecomment-339841781

    Args:
        flavor_text: Raw flavor text as stored in the Pokedex dataset.

    Returns:
        A normalized, human-readable flavor text string.
    """
    text = (
        flavor_text.replace("\f", "\n")  # page breaks -> newline
        .replace("\u00ad\n", "")  # soft hyphen + newline disappears
        .replace("\u00ad", "")  # remaining soft hyphens disappear
        .replace(" -\n", " - ")  # preserve " - " across line breaks
        .replace("-\n", "-")  # preserve real hyphenation
        .replace("\n", " ")
    )  # remaining newlines -> spaces

    return " ".join(text.split())  # collapse whitespace


def to_domain_pokemon_info(dto: PokeApiSpeciesDTO) -> Pokemon:
    """Converts a pokeapi pokemon into a domain pokemon object."""
    # Safely extract description
    description = next(
        (
            entry.flavor_text
            for entry in dto.flavor_text_entries or []
            if entry.language.name == settings.preferred_language
        ),
        dto.flavor_text_entries[0].flavor_text,
    )

    # Safely extract habitat
    habitat = dto.habitat.name if dto.habitat else None

    return Pokemon(
        name=dto.name,
        description=normalize_flavor_text(description),
        habitat=habitat,
        isLegendary=dto.is_legendary,
    )
