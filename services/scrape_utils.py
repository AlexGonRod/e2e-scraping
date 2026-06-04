import time

import httpx
import requests

from lib.config import TendiosConfig


def fill_form(self, url, form_selectors):
    try:
        self.page.goto(url, wait_until="networkidle")

        # Rellenar campos del formulario
        for selector, value in form_selectors.items():
            if isinstance(value, list):
                for cpv in value:
                    print(f"Rellenando {selector}: {cpv}")
                    self.page.fill(selector, str(cpv))
                    self.page.eval_on_selector(
                        ".commandLink.marginLeft0punto4.nodecoration  ",
                        "element => element.click()",
                    )
                    time.sleep(3)
            elif value == "click":
                print(f"Haciendo click en: {selector}")
                self.page.click(selector)
            else:
                print(f"Seleccionando {selector}: {value}")
                self.page.select_option(selector, value)
                time.sleep(3)

        # Esperar a que carguen los resultados
        self.page.wait_for_load_state("networkidle")
        time.sleep(5)

        return self.page.content()

    except Exception as e:
        print(f"Error rellenando formulario: {e}")
        raise RuntimeError("Error rellenando formulario") from e


def extract_data(self, selector, attribute=None):
    if not selector:
        raise ValueError("El selector no puede estar vacío")

    elements = self.page.query_selector_all(selector)

    data = []
    for elem in elements:
        if attribute:
            value = elem.get_attribute(attribute)
        else:
            value = elem.inner_text()
        data.append(value)

    return data


def extract_table(self, table_selector="table"):
    """Extrae datos de una tabla HTML"""
    try:
        # Esperar a que la tabla exista
        self.page.wait_for_selector(table_selector, timeout=10000)
        table_data = self.page.evaluate(f"""
            () => {{
                const table = document.querySelector('{table_selector}');
                if (!table) return [];

                const rows = Array.from(table.querySelectorAll('tbody tr'));

                const parseNumber = (text) => {{
                    if (!text) return null;
                    let cleaned = text.replace(/[^\\d.,-]/g, '');
                    const dots = (cleaned.match(/\\./g) || []).length;
                    const commas = (cleaned.match(/,/g) || []).length;
                    if (dots > 1 || (dots === 1 && commas > 0)) {{
                        cleaned = cleaned.replace(/\\./g, '').replace(',', '.');
                    }} else if (commas > 0) {{
                        cleaned = cleaned.replace(',', '.');
                    }}
                    const num = parseFloat(cleaned);
                    return isNaN(num) ? null : num;
                }};

                return rows.map(row => {{
                    const cells = Array.from(row.querySelectorAll('td'));
                    if (cells.length < 1) return null;

                    const firstCell = cells[0];
                    const expedient = firstCell.querySelector('span[id*="textoEnlace"]')?.innerText.trim() || "";
                    const name = firstCell.querySelector('div:nth-child(2)')?.innerText.trim() || "";
                    const anchor = firstCell.querySelector('div.cell-order > a');
                    const onClickText = anchor ? anchor.getAttribute('onclick') : "";
                    const idMatch = onClickText ? onClickText.match(/'idLicitacion','(\\d+)'/) : null;
                    const id = idMatch ? idMatch[1] : "";

                    return {{
                        "id": id,
                        "expedient": expedient,
                        "name": name,
                        "budgetNoTaxes": parseNumber(cells[3]?.innerText) || 0,
                        "awardAmount": null,
                        "status": cells[2]?.innerText.trim() || "",
                        "location": cells[1]?.innerText.trim() || "",
                        "contractingOrganization": {{
                            "id": "",
                            "name": cells[5]?.innerText.trim() || ""
                        }},
                        "numLots": 0,
                        "expedientPublishedAt": cells[4]?.innerText.trim() || "",
                        "expedientSubmissionDeadline": ""
                    }};
                }}).filter(item => item !== null);
            }}
        """)  # noqa: E501
        final_json = {"data": table_data}
        return final_json

    except Exception as e:
        print(f"Error extrayendo tabla: {e}")
        return []


def get_deeplink(id, headers) -> dict:
    try:
        deeplink = f"{TendiosConfig.api_url}/api/tenders/{id}/sources"
        response = requests.get(deeplink, headers=headers, timeout=10).json()
        if (
            not response
            or not isinstance(response, list)
            or "linkUrl" not in response[0]
        ):
            raise RuntimeError(f"Respuesta inesperada al obtener deeplink: {response}")

        return response[0]["linkUrl"]
    except Exception as e:
        print(f"Error obteniendo deeplink: {e}")
        raise RuntimeError("Error obteniendo deeplink") from e


async def async_get_deeplink(id, headers) -> dict:
    try:
        deeplink = f"{TendiosConfig.api_url}/api/tenders/{id}/sources"
        async with httpx.AsyncClient() as client:
            response = (await client.get(deeplink, headers=headers, timeout=10)).json()
        if (
            not response
            or not isinstance(response, list)
            or "linkUrl" not in response[0]
        ):
            raise RuntimeError(f"Respuesta inesperada al obtener deeplink: {response}")

        return response[0]["linkUrl"]
    except Exception as e:
        print(f"Error obteniendo deeplink: {e}")
        raise RuntimeError("Error obteniendo deeplink") from e
