"""Cache keys for pokemon state."""

import hashlib

from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.settings import get_logger

# logger
logger = get_logger()


def _stable_text_hash(text: str) -> str:
    """Stable hash for pokemon state."""
    normalized = " ".join(text.split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def pokemon_species_key(name: str) -> str:
    """Pokemon species key for pokemon state."""
    key = f"pokemon_species:{name.strip().lower()}"
    logger.debug(f"cached pokemon_species_key: {key}")
    return key


def translation_key(text: str, strategy: TranslationStrategy) -> str:
    """Translation key for pokemon state."""
    # hash to avoid long keys
    digest = _stable_text_hash(text)
    key = f"translation:{strategy.value}:{digest}"
    logger.debug(f"cached translation_key: {key}")
    return key
