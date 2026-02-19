import json
import functools

def save_data_to_json(fn):

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs) -> None:
        data = fn(self,*args, **kwargs)
        filename = getattr(self, 'filename', "form_results.json")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Datos guardados en {filename}")
        return data
    return wrapper
