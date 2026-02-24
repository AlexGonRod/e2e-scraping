import requests
from lib.config import TendiosConfig

def tendios_model() -> dict:

    response = requests.post(f'{TendiosConfig.api_url}/api/searcher-tender', headers=TendiosConfig.headers, json=TendiosConfig.payload, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Error en la llamada a la API: {response.status_code}")

    return response.json()
