"""Translation strategy."""

from enum import Enum

from pokedex.domains.pokemon.model import Pokemon


class TranslationStrategy(str, Enum):
    """Translation strategy."""

    SHAKESPEARE = "shakespeare"
    YODA = "yoda"


class TranslationStrategyPolicy:
    """Business rules to decide translation strategy."""

    def choose(self, pokemon: Pokemon) -> TranslationStrategy:
        """Choose a translation strategy."""
        if pokemon.is_legendary or (pokemon.habitat == "cave"):
            return TranslationStrategy.YODA
        return TranslationStrategy.SHAKESPEARE
