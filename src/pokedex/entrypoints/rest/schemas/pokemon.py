"""Pokemon schemas for REST API."""

from pydantic import BaseModel

from pokedex.domains.pokemon import model


class GetPokemonResponse(BaseModel):
    """Get pokemon response schema."""

    pokemon: model.Pokemon
