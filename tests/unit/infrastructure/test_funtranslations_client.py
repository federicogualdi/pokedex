"""Tests for Funtranslations client."""

import httpx
import pytest

from httpx import MockTransport
from httpx import Request
from httpx import Response

from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.infrastructure.http.clients.funtranslations.client import FuntranslationsApiClient
from pokedex.shared.exceptions import ExecutionError
from tests.data.funtranslations_data_generators import funtranslations_success
from tests.unit.infrastructure.utils import FUNTRANSLATION_BASE
from tests.unit.infrastructure.utils import TRANSLATION_STRATEGY
from tests.unit.infrastructure.utils import transport_json


@pytest.mark.asyncio
async def test_shakespeare_translation_parses_translated_text():
    """200 response is parsed and translated text is returned."""
    # Arrange
    transport = transport_json(200, funtranslations_success(translated="To be, or not to be.").model_dump())
    async with httpx.AsyncClient(transport=transport, base_url=FUNTRANSLATION_BASE) as http:
        client = FuntranslationsApiClient(http=http, base_url=FUNTRANSLATION_BASE, translators=TRANSLATION_STRATEGY)

        # Act
        out = await client.translate("Hello", TranslationStrategy.SHAKESPEARE)

    # Assert
    assert out == "To be, or not to be."


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 429, 500, 503])
async def test_shakespeare_translation_maps_http_errors_to_execution_error(status_code: int):
    """Non-2xx responses are mapped to ExecutionError."""
    # Arrange
    transport = transport_json(status_code, {"detail": "x"})
    async with httpx.AsyncClient(transport=transport, base_url=FUNTRANSLATION_BASE) as http:
        client = FuntranslationsApiClient(http=http, base_url=FUNTRANSLATION_BASE, translators=TRANSLATION_STRATEGY)

        # Act / Assert
        with pytest.raises(ExecutionError):
            await client.translate("Hello", TranslationStrategy.SHAKESPEARE)


@pytest.mark.asyncio
async def test_shakespeare_translation_maps_network_errors_to_execution_error():
    """Network errors are mapped to ExecutionError."""

    # Arrange
    def handler(_: Request) -> Response:
        raise httpx.ConnectError(
            "boom",
            request=Request("POST", f"{FUNTRANSLATION_BASE}/shakespeare"),
        )

    transport = MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url=FUNTRANSLATION_BASE) as http:
        client = FuntranslationsApiClient(http=http, base_url=FUNTRANSLATION_BASE, translators=TRANSLATION_STRATEGY)

        # Act / Assert
        with pytest.raises(ExecutionError):
            await client.translate("Hello", TranslationStrategy.SHAKESPEARE)
