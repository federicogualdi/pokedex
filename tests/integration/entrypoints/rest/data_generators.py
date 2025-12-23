"""Data generator for pokemon integration test."""

from tests.data.pokeapi_data_generators import flavor_en
from tests.data.pokeapi_data_generators import flavor_it
from tests.data.pokeapi_data_generators import pokeapi_species_payload


def expected_pokemon_response(
    *,
    name: str,
    description: str,
    habitat: str | None,
    is_legendary: bool,
) -> dict:
    """Build a Pokémon species payload for tests."""
    return {
        "pokemon": {
            "name": name,
            "description": description,
            "habitat": habitat,
            "isLegendary": is_legendary,
        },
    }


HAPPY_CASES = [
    (
        "mewtwo",
        pokeapi_species_payload(
            name="mewtwo",
            habitat="rare",
            is_legendary=True,
            flavor_entries=[flavor_it("ciao"), flavor_en("A test\ntext.\f")],
        ),
        expected_pokemon_response(
            name="mewtwo",
            description="A test text.",
            habitat="rare",
            is_legendary=True,
        ),
    ),
    (
        "pikachu",
        pokeapi_species_payload(
            name="pikachu",
            habitat="forest",
            is_legendary=False,
            flavor_entries=[flavor_en("Electric mouse.")],
        ),
        expected_pokemon_response(
            name="pikachu",
            description="Electric mouse.",
            habitat="forest",
            is_legendary=False,
        ),
    ),
]

CORNER_CASES = [
    (
        "no-en-description",
        pokeapi_species_payload(
            name="no-en-description",
            habitat="grassland",
            is_legendary=False,
            flavor_entries=[flavor_it("solo italiano")],
        ),
        expected_pokemon_response(
            name="no-en-description",
            description="solo italiano",
            habitat="grassland",
            is_legendary=False,
        ),
    ),
    (
        "no-habitat",
        pokeapi_species_payload(
            name="no-habitat",
            habitat=None,
            is_legendary=False,
            flavor_entries=[flavor_en("Hello")],
        ),
        expected_pokemon_response(
            name="no-habitat",
            description="Hello",
            habitat=None,
            is_legendary=False,
        ),
    ),
]

ERROR_HTTP_CASES = [
    # upstream 404 -> API 404
    (404, 404),
    # upstream 5xx -> API 503
    (500, 503),
    (503, 503),
]
