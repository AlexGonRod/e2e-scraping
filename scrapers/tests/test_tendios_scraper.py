from unittest.mock import AsyncMock

import pytest

from controllers.scraper_controller import ScraperController
from scrapers.tendios import FetchDataTendios

filename = "Test.json"

@pytest.mark.asyncio
async def test_fetch_tendios_returns_data():
    mockController = AsyncMock(ScraperController)
    mockController.scrape.return_value = {"data": [{"id": 1, "title": "Test"}]}

    fetcher = FetchDataTendios(mockController)
    fetcher.filename = filename

    result = await fetcher.fetch()
    assert result == {"data": [{"id": 1, "title": "Test"}]}

@pytest.mark.asyncio
async def test_tendios_fetch_data_no_filename():
    mockController = AsyncMock(ScraperController)
    mockController.scrape.return_value = {"data": [{"id": 1, "title": "Test"}]}

    fetcher = FetchDataTendios(mockController)
    fetcher.filename = None

    result = await fetcher.fetch()
    assert result == {"data": [{"id": 1, "title": "Test"}]}

@pytest.mark.asyncio
async def test_tendios_returns_empty_API():
    mock_controller = AsyncMock(ScraperController)
    mock_controller.scrape.return_value = {"data":[]}

    fetcher = FetchDataTendios(mock_controller)
    fetcher.filename = filename

    result = await fetcher.fetch()
    assert result == {"data":[]}

@pytest.mark.asyncio
async def test_tendios_returns_API_error():
    mockController = AsyncMock(ScraperController)
    mockController.scrape.side_effect = RuntimeError("API error")

    fetcher = FetchDataTendios(mockController)
    fetcher.filename = None

    with pytest.raises(RuntimeError, match="API error"):
        await fetcher.fetch()
