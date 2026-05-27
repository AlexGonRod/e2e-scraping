import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class TendiosConfig:
    token: str = os.getenv("BEARER_TOKEN") or ""
    url: str = os.getenv("URL") or ""
    api_url: str = os.getenv("API_URL") or ""
    status: List[str] = ["Publicada"]
    # cpvs_codes: List[str] = ['15713000','15712000','35250000','44619300','45223600','80512000']
    cpvs_codes: List[str] = [
        "24600000",
        "38546000",
        "39500000",
        "44423000",
        "44619300",
        "80512000",
    ]

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "es-ES,es;q=0.9",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": f"{url}",
        "priority": "u=1, i",
        "sec-ch-ua-platform": '"macOS"',
        "referer": f"{url}",
        "sec-ch-ua": '"Chromium";v="142", "Brave";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "x-app-type": "bid",
    }
    payload = {
        "page": 1,
        "pageSize": 10,
        "sort": "by-published-date",
        "isDescendent": True,
        "cpvs": cpvs_codes,
        "status": status,
        "isOnlyWithinDeadline": True,
        "isMinorContract": None,
    }
