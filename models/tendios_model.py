import httpx
from lib.config import TendiosConfig
from services.scrape_utils import async_get_deeplink


class TendiosModel:
    async def get(self) -> dict:
        async with httpx.AsyncClient() as client:
            response = (
                await client.post(
                    f"{TendiosConfig.api_url}/api/searcher-tender",
                    headers=TendiosConfig.headers,
                    json=TendiosConfig.payload,
                    timeout=10,
                )
            ).json()
        if response.get("status_code", 200) != 200:
            raise RuntimeError(
                f"Error en la llamada a la API: {
                    response.get('status_code', 'Unknown')
                }"
            )

        data = response.get("data", [])
        for item in data:
            link = await async_get_deeplink(item["id"], headers=TendiosConfig.headers)
            item["linkUrl"] = link
        return data
