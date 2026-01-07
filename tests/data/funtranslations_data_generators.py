"""Helper file to build funtranslations data."""

from pokedex.infrastructure.http.clients.funtranslations.schemas import FuntranslationsResponse
from pokedex.infrastructure.http.clients.funtranslations.schemas import FuntranslationsResponseContents


def funtranslations_success(*, translated: str) -> FuntranslationsResponse:
    """Build a successful Funtranslations response DTO."""
    return FuntranslationsResponse(contents=FuntranslationsResponseContents(translated=translated))
