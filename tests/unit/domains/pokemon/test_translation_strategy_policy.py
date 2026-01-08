"""Test for translation strategy."""

import pytest

from pokedex.domains.pokemon.model import Pokemon
from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.domains.pokemon.translation_strategy import TranslationStrategyPolicy


@pytest.mark.parametrize(
    ("habitat", "is_legendary", "expected"),
    [
        ("forest", False, TranslationStrategy.SHAKESPEARE),
        ("cave", False, TranslationStrategy.YODA),
        ("forest", True, TranslationStrategy.YODA),
        (None, True, TranslationStrategy.YODA),
    ],
)
def test_translation_strategy_policy_choose(habitat: str | None, is_legendary: bool, expected: TranslationStrategy):
    """Test translation strategy policy."""
    # Arrange
    policy = TranslationStrategyPolicy()
    pokemon = Pokemon(
        name="x",
        description="desc",
        habitat=habitat,
        isLegendary=is_legendary,
    )

    # Act
    out = policy.choose(pokemon)

    # Assert
    assert out == expected
