import requests
from lib.config import TendiosConfig
from services.scrape_utils import get_deeplink

class TendiosModel():

    def get(self) -> dict:
        response = requests.post(f'{TendiosConfig.api_url}/api/searcher-tender', headers=TendiosConfig.headers, json=TendiosConfig.payload, timeout=10).json()
        if response.get("status_code", 200) != 200:
            raise RuntimeError(f"Error en la llamada a la API: {response.get('status_code', 'Unknown')}")

        data = response.get("data", [])
        for item in data:
            response = get_deeplink(item['id'], headers=TendiosConfig.headers)
            item['linkUrl'] = response
        return data
