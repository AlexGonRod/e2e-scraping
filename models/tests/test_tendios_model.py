from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from models.tendios_model import TendiosModel


@pytest.mark.asyncio
async def test_get_tendios__response():
    mockClient = AsyncMock(spec=httpx.AsyncClient)
    mockClient.__aenter__.return_value = mockClient

    mockResponse = MagicMock()
    mockResponse.json.return_value = {"data": [{"id":1}], "status_code": 200}
    mockClient.post.return_value = mockResponse

    with patch("models.tendios_model.return_deeplink") as mockDeepLink:
        mockDeepLink.return_value =  [{"id": 1, "linkUrl": "https://link.com"}]
        model = TendiosModel(client=mockClient)
        result = await model.get()

    assert result == [{"id": 1, "linkUrl": "https://link.com"}]

@pytest.mark.asyncio
async def test_raise_error():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.__aenter__.return_value = mock_client

    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"id":1}], "status_code": 400}
    mock_client.post.return_value = mock_response


    with pytest.raises(RuntimeError, match="Error en la llamada a la API: 400"):
        model = TendiosModel(client=mock_client)
        await model.get()
