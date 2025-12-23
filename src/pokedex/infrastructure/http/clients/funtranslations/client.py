"""Pokeapi Http Client."""

from typing import TypeVar

import httpx

from pokedex.domains.pokemon.ports import TranslationPort
from pokedex.infrastructure.http.base_http_client_adapter import BaseHttpClientAdapter
from pokedex.infrastructure.http.clients.funtranslations.schemas import FuntranslationsRequest
from pokedex.infrastructure.http.clients.funtranslations.schemas import FuntranslationsResponse
from pokedex.settings import get_logger
from pokedex.settings import settings

# logger
logger = get_logger()

T = TypeVar("T")


class FuntranslationsApiClient(BaseHttpClientAdapter, TranslationPort):
    """Funtranslations Http Client."""

    client_name = "Funtranslations"

    def __init__(self, http: httpx.AsyncClient, base_url: str):
        """Initializes FuntranslationsApiClient."""
        super().__init__(http, base_url)

    async def shakespeare_translation(self, text: str) -> str:
        """Apply shakespeare translation to text."""
        response = await self._request(
            method="POST",
            path=f"/{settings.funtranslations_shakespeare_path}",
            json=FuntranslationsRequest(text=text).model_dump(),
        )
        dto = FuntranslationsResponse.model_validate(response.json())
        return dto.contents.translated
