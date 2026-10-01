import httpx

from lib.config import TendiosConfig
from services.scrape_utils import async_get_deeplink


async def return_deeplink(data: list, headers: dict) -> list:

    for item in data:
        link = await async_get_deeplink(item["id"], headers= headers)
        item["linkUrl"] = link

    return data

class TendiosModel:
    def __init__(self, client: httpx.AsyncClient | None = None):
        self._client = client

    async def get(self) -> dict:
        async with self._client or httpx.AsyncClient() as c:
            resp = await c.post(
                f"{TendiosConfig.api_url}/api/alerts/698085bc71d27258857c4d28/tenders",
                headers=TendiosConfig.headers,
                json=TendiosConfig.payload,
                timeout=10,
            )
        print(f"Status: {resp.status_code}")
        print(f"Headers: {dict(resp.headers)}")
        response = resp.json()
        print(f"Full response: {response}")
        if response.get("status_code", 200) != 200:
            raise RuntimeError(
                f"Error en la llamada a la API: {response.get('status_code', 'Unknown')}"
            )
        print(f"Data: {response.get('data', [])}")
        return await return_deeplink(response.get("data", []), TendiosConfig.headers)
