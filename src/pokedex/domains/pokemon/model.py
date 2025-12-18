"""Pokemon models."""

from pydantic import BaseModel
from pydantic import Field


class Pokemon(BaseModel):
    """Pokemon model."""

    name: str = Field()
    description: str = Field()
    habitat: str | None = Field()
    is_legendary: bool = Field(alias="isLegendary")
