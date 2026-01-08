"""Test for strategy funtranslations client."""

import httpx
import pytest

from _pytest.monkeypatch import MonkeyPatch

from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.infrastructure.http.clients.funtranslations.client import FuntranslationsApiClient
from pokedex.settings import settings
from pokedex.shared.exceptions import ExecutionError
from tests.data.funtranslations_data_generators import funtranslations_success
from tests.unit.infrastructure.utils import FUNTRANSLATION_BASE
from tests.unit.infrastructure.utils import TRANSLATION_STRATEGY
from tests.unit.infrastructure.utils import transport_json


@pytest.mark.asyncio
async def test_funtranslations_translate_shakespeare_parses_translated_text(monkeypatch: MonkeyPatch):
    """Test shakespeareare parses translated text."""
    # Arrange

    monkeypatch.setattr(settings, "funtranslations_shakespeare_path", "shakespeare")

    payload = funtranslations_success(translated="Translated").model_dump()
    transport = transport_json(200, payload)

    async with httpx.AsyncClient(transport=transport, base_url=FUNTRANSLATION_BASE) as http:
        client = FuntranslationsApiClient(http=http, base_url=FUNTRANSLATION_BASE, translators=TRANSLATION_STRATEGY)

        # Act
        out = await client.translate("Original", TranslationStrategy.SHAKESPEARE)

    # Assert
    assert out == "Translated"


@pytest.mark.asyncio
async def test_funtranslations_translate_yoda_raises_execution_error():
    """Test funtranslations translate raises execution error."""
    # Arrange
    async with httpx.AsyncClient(transport=transport_json(200, {}), base_url=FUNTRANSLATION_BASE) as http:
        client = FuntranslationsApiClient(http=http, base_url=FUNTRANSLATION_BASE, translators=TRANSLATION_STRATEGY)

        # Act / Assert
        with pytest.raises(ExecutionError):
            await client.translate("Original", TranslationStrategy.YODA)
