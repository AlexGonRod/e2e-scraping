from unittest.mock import MagicMock

import pytest

from scrapers.estado import ScraperModel


def test_scrape_raises_when_page_is_None():
    mock_model = MagicMock()
    mock_model.page = None

    model = ScraperModel(mock_model)

    with pytest.raises(RuntimeError, match="No se pudo inicializar la página de Playwright"):
        model.scrape()
