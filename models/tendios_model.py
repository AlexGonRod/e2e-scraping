import os
from typing import List
from dotenv import load_dotenv
import requests

load_dotenv()
token: str = os.getenv('BEARER_TOKEN') or ''
url: str = os.getenv('URL') or ''
api_url: str = os.getenv('API_URL') or ''
status: List[str] = ['Publicada']

def tendios_model(cpvs_codes: List[str], url: str = url, status: List[str] = status) -> dict:
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'es-ES,es;q=0.9',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': f'{url}',
        'priority': 'u=1, i',
        'sec-ch-ua-platform': '"macOS"',
        'referer': f'{url}',
        'sec-ch-ua': '"Chromium";v="142", "Brave";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'x-app-type': 'bid',
    }

    payload = {
        'page': 1,
        'pageSize': 10,
        'sort': 'by-published-date',
        'isDescendent': True,
        'cpvs': cpvs_codes,
        'status': status,
        'isOnlyWithinDeadline': True,
        'isMinorContract': None,
    }
    response = requests.post(f'{api_url}/api/searcher-tender', headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Error en la llamada a la API: {response.status_code}")

    return response.json()
