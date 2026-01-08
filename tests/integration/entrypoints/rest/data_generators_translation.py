"""Data generator for pokemon translated integration tests."""

from tests.data.pokeapi_data_generators import flavor_en
from tests.data.pokeapi_data_generators import pokeapi_species_payload


def expected_pokemon_response(
    *,
    name: str,
    description: str,
    habitat: str | None,
    is_legendary: bool,
) -> dict:
    """Build the expected API response for a Pokemon."""
    return {
        "pokemon": {
            "name": name,
            "description": description,
            "habitat": habitat,
            "isLegendary": is_legendary,
        },
    }


# Happy path: translation applied
TRANSLATED_HAPPY_CASES = [
    (
        "pikachu",
        pokeapi_species_payload(
            name="pikachu",
            habitat="forest",
            is_legendary=False,
            flavor_entries=[flavor_en("Electric mouse.")],
        ),
        "Translated description.",
        expected_pokemon_response(
            name="pikachu",
            description="Translated description.",
            habitat="forest",
            is_legendary=False,
        ),
    ),
    (
        "mewtwo",
        pokeapi_species_payload(
            name="mewtwo",
            habitat="rare",
            is_legendary=True,
            flavor_entries=[flavor_en("Original description.")],
        ),
        "Translated description.",
        expected_pokemon_response(
            name="mewtwo",
            description="Translated description.",
            habitat="rare",
            is_legendary=True,
        ),
    ),
]


# Fallback path: translation fails -> keep original description (still 200)
TRANSLATED_FALLBACK_CASES = [
    (
        "pikachu",
        pokeapi_species_payload(
            name="pikachu",
            habitat="forest",
            is_legendary=False,
            flavor_entries=[flavor_en("Original description.")],
        ),
        429,  # Funtranslations upstream status
        expected_pokemon_response(
            name="pikachu",
            description="Original description.",
            habitat="forest",
            is_legendary=False,
        ),
    ),
    (
        "bulbasaur",
        pokeapi_species_payload(
            name="bulbasaur",
            habitat="grassland",
            is_legendary=False,
            flavor_entries=[flavor_en("Original description.")],
        ),
        500,
        expected_pokemon_response(
            name="bulbasaur",
            description="Original description.",
            habitat="grassland",
            is_legendary=False,
        ),
    ),
]
