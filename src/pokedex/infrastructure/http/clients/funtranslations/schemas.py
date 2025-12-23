"""Pokeapi http client schemas."""

from pydantic import BaseModel


class FuntranslationsRequest(BaseModel):
    """Funtranslations request."""

    text: str


class FuntranslationsResponseContents(BaseModel):
    """Funtranslations Response contents model."""

    translated: str


class FuntranslationsResponse(BaseModel):
    """Funtranslations response."""

    contents: FuntranslationsResponseContents
