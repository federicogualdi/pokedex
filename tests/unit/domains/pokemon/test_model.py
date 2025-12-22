"""Test for Pokemon domain object."""

import pytest

from pydantic import ValidationError

from pokedex.domains.pokemon.model import Pokemon


def test_pokemon_accepts_alias_isLegendary():  # noqa: N802
    """Accept the 'isLegendary' alias when building the model from external payloads."""
    p = Pokemon(name="mewtwo", description="desc", habitat="cave", isLegendary=True)
    assert p.is_legendary is True


def test_pokemon_rejects_field_name_if_alias_only():
    """Reject 'is_legendary' input if population by field name is disabled."""
    with pytest.raises(ValidationError):
        Pokemon(name="mewtwo", description="desc", habitat="cave", is_legendary=True)


def test_pokemon_allows_null_habitat():
    """Allow habitat to be null/None."""
    p = Pokemon(name="mewtwo", description="desc", habitat=None, isLegendary=False)
    assert p.habitat is None


@pytest.mark.parametrize(
    "bad_payload",
    [
        {"name": 123, "description": "desc", "habitat": "cave", "isLegendary": True},  # wrong name format
        {"name": "mewtwo", "description": None, "habitat": "cave", "isLegendary": True},  # no description
        {"name": "mewtwo", "description": "desc", "habitat": 999, "isLegendary": True},  # wrong habitat format
        {"description": "desc", "habitat": "cave", "isLegendary": True},  # missing name
        {"name": "mewtwo", "habitat": "cave", "isLegendary": True},  # missing description
        {"name": "mewtwo", "description": "desc", "habitat": "cave"},  # missing isLegendary
    ],
)
def test_pokemon_validation_errors(bad_payload: dict):
    """Raise ValidationError for missing fields or invalid types."""
    with pytest.raises(ValidationError):
        Pokemon(**bad_payload)


def test_pokemon_serializes_with_alias():
    """Dump using aliases so the public schema uses 'isLegendary'."""
    p = Pokemon(name="mewtwo", description="desc", habitat="cave", isLegendary=True)

    # Pydantic v2: model_dump(by_alias=True)
    # Pydantic v1: dict(by_alias=True)
    dumped = p.model_dump(by_alias=True)

    assert "isLegendary" in dumped
    assert dumped["isLegendary"] is True
    assert "is_legendary" not in dumped
