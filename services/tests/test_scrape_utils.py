import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from playwright.sync_api import sync_playwright
from controllers.playwright_controller import PlaywrightController
from services.scrape_utils import get_deeplink

@pytest.fixture
def controller():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.set_content(Path("services/tests/mock_html/mock_html.html").read_text())
        yield PlaywrightController(page)
        browser.close()

def test_extract_data_no_attr(controller):
    result = controller.extract_data("h1")
    assert result == ["Test Utils"]

def test_extract_data_with_attr(controller):
    result = controller.extract_data("h2", "aria-atomic")
    assert result == ["false"]

def test_extract_data_no_selector(controller):
    with pytest.raises(ValueError, match="El selector no puede estar vacío"):
        controller.extract_data("")

def test_extract_data_nonexistent_selector(controller):
    result = controller.extract_data("h3")
    assert result == []

def test_get_deeplink():
    mock_response = MagicMock()
    mock_response.json.return_value = [{"linkUrl": "https://example.com/tender/123"}]
    
    with patch("services.scrape_utils.requests.get", return_value = mock_response):
        result = get_deeplink("123", headers={"Authorization": "Bearer token"})
    
    assert result == "https://example.com/tender/123"

def test_get_deeplinkk_raise_exception():

    with patch("services.scrape_utils.requests.get", side_effect = Exception("ERROR")):
        with pytest.raises(RuntimeError, match="Error obteniendo deeplink"):
            get_deeplink("123", headers={"Authorization": "Bearer token"})

def test_get_deeplink_raise_no_link():
    mock_response = MagicMock()
    mock_response.json.return_value = []

    with patch("services.scrape_utils.requests.get", return_value = mock_response):
        with pytest.raises(RuntimeError, match="Error obteniendo deeplink"):
            get_deeplink("123", headers={"Authorization": "Bearer token"})


def test_get_deeplink_raise_no_list():
    mock_response = MagicMock()
    mock_response.json.return_value = {}

    with patch("services.scrape_utils.requests.get", return_value = mock_response):
        with pytest.raises(RuntimeError, match="Error obteniendo deeplink"):
            get_deeplink("123", headers={"Authorization": "Bearer token"})

def test_get_deeplink_raise_not_linkUrl():
    mock_response = MagicMock()
    mock_response.json.return_value = [{"notLink": "https://example.com/tender/123"}]

    with patch("services.scrape_utils.requests.get", return_value = mock_response):
        with pytest.raises(RuntimeError, match="Error obteniendo deeplink"):
            get_deeplink("123", headers={"Authorization": "Bearer token"})