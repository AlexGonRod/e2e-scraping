import inspect
import json
import functools


def save_data_to_json(fn):
    if inspect.iscoroutinefunction(fn):

        @functools.wraps(fn)
        async def async_wrapper(self, *args, **kwargs):
            data = await fn(self, *args, **kwargs)
            filename = getattr(self, "filename", "form_results.json")
            if not filename:
                print("No se proporcionó un nombre de archivo válido. Se guardarán los datos en form_results.json")
                return data
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Datos guardados en {filename}")
            return data

        return async_wrapper

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        data = fn(self, *args, **kwargs)
        filename = getattr(self, "filename", "form_results.json")
        if not filename:
            print("No se proporcionó un nombre de archivo válido. Se guardarán los datos en form_results.json")
            return data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Datos guardados en {filename}")
        return data

    return wrapper
