import asyncio
import json
import functools
from datetime import datetime

def save_data_to_json(fn):
    if asyncio.iscoroutinefunction(fn):
        @functools.wraps(fn)
        async def async_wrapper(self, *args, **kwargs):
            data = await fn(self, *args, **kwargs)
            filename = getattr(self, 'filename', "form_results.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Datos guardados en {filename}")
            return data
        return async_wrapper

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        data = fn(self, *args, **kwargs)
        filename = getattr(self, 'filename', "form_results.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Datos guardados en {filename}")
        return data
    return wrapper

def format_date(date_str: str) -> str:
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return date_str
