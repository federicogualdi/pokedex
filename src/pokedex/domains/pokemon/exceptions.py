"""Error definition for Pokemon Domain."""

from pokedex.shared.exceptions import NotFoundError


class PokemonNotFoundError(NotFoundError):
    """Pokemon not found."""

    def __init__(self, pokemon_name: str):
        """Pokemon not found."""
        super().__init__(f"Pokemon '{pokemon_name}' not found")
        self.pokemon_name = pokemon_name
