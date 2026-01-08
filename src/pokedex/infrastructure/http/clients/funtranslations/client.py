"""Pokeapi Http Client."""

import abc

from collections.abc import Awaitable
from collections.abc import Callable
from typing import TypeVar

import httpx

from pokedex.domains.pokemon.ports import TranslationPort
from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.infrastructure.http.base_http_client_adapter import BaseHttpClientAdapter
from pokedex.infrastructure.http.clients.funtranslations.schemas import FuntranslationsRequest
from pokedex.infrastructure.http.clients.funtranslations.schemas import FuntranslationsResponse
from pokedex.settings import get_logger
from pokedex.settings import settings
from pokedex.shared.exceptions import ExecutionError

# logger
logger = get_logger()

T = TypeVar("T")
RequestFn = Callable[..., Awaitable[httpx.Response]]


class FunTranslator(abc.ABC):
    """Funtranslations Base Http Client."""

    strategy: TranslationStrategy

    @abc.abstractmethod
    async def translate(self, request: RequestFn, text: str) -> str:
        """Abstract method to translate text."""


class ShakespeareTranslator(FunTranslator):
    """Funtranslations Shakespeare Http Client."""

    strategy = TranslationStrategy.SHAKESPEARE

    async def translate(self, request: RequestFn, text: str) -> str:
        """Translate text using Shakespeare."""
        response = await request(
            method="POST",
            path=settings.funtranslations_shakespeare_path,
            json=FuntranslationsRequest(text=text).model_dump(),
        )
        dto = FuntranslationsResponse.model_validate(response.json())
        return dto.contents.translated


class FuntranslationsApiClient(BaseHttpClientAdapter, TranslationPort):
    """Funtranslations Http Client."""

    client_name = "Funtranslations"

    def __init__(self, http: httpx.AsyncClient, base_url: str, translators: list[FunTranslator]):
        """Initializes FuntranslationsApiClient."""
        super().__init__(http, base_url)
        self._registry = {t.strategy: t for t in translators}

    async def translate(self, text: str, strategy: TranslationStrategy) -> str:
        """Translate text using funtranslations."""
        t = self._registry.get(strategy)
        if not t:
            raise ExecutionError(f"{self.client_name}: strategy not supported: {strategy}")
        return await t.translate(self._request, text)
