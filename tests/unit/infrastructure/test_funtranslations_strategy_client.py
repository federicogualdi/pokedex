"""Test for strategy funtranslations client."""

import httpx
import pytest

from pokedex.domains.pokemon.translation_strategy import TranslationStrategy
from pokedex.infrastructure.http.clients.funtranslations.client import FuntranslationsApiClient
from tests.data.funtranslations_data_generators import funtranslations_success
from tests.unit.infrastructure.utils import FUNTRANSLATION_BASE
from tests.unit.infrastructure.utils import TRANSLATION_STRATEGY
from tests.unit.infrastructure.utils import transport_json


@pytest.mark.asyncio
async def test_funtranslations_translate_shakespeare_parses_translated_text():
    """Test shakespeareare parses translated text."""
    # Arrange
    payload = funtranslations_success(translated="Translated").model_dump()
    transport = transport_json(200, payload)

    async with httpx.AsyncClient(transport=transport, base_url=FUNTRANSLATION_BASE) as http:
        client = FuntranslationsApiClient(http=http, base_url=FUNTRANSLATION_BASE, translators=TRANSLATION_STRATEGY)

        # Act
        out = await client.translate("Original", TranslationStrategy.SHAKESPEARE)

    # Assert
    assert out == "Translated"


@pytest.mark.asyncio
async def test_funtranslations_translate_yoda_parses_translated_text():
    """Test yoda parses translated text."""
    # Arrange
    payload = funtranslations_success(translated="Translated").model_dump()
    transport = transport_json(200, payload)

    async with httpx.AsyncClient(transport=transport, base_url=FUNTRANSLATION_BASE) as http:
        client = FuntranslationsApiClient(http=http, base_url=FUNTRANSLATION_BASE, translators=TRANSLATION_STRATEGY)

        # Act
        out = await client.translate("Original", TranslationStrategy.YODA)

    # Assert
    assert out == "Translated"
