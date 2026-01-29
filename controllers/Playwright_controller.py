from playwright.sync_api import Page
import time

class PlaywrightController:

    def __init__(self,page: Page):
        self.page = page

    def fill_form_and_scrape(self, url, form_selectors):
        try:
            self.page.goto(url, wait_until='networkidle')

            # Rellenar campos del formulario
            for selector, value in form_selectors.items():
                if isinstance(value, list):
                    for cpv in value:
                        print(f"Rellenando {selector}: {cpv}")
                        self.page.fill(selector, str(cpv))
                        self.page.eval_on_selector('.commandLink.marginLeft0punto4.nodecoration  ', "element => element.click()")
                        time.sleep(3)
                elif value == 'click':
                    print(f"Haciendo click en: {selector}")
                    self.page.click(selector)
                else:
                    print(f"Seleccionando {selector}: {value}")
                    self.page.select_option(selector, value)
                    time.sleep(3)

            # Esperar a que carguen los resultados
            self.page.wait_for_load_state('networkidle')
            time.sleep(5)

            return self.page.content()

        except Exception as e:
            print(f"Error rellenando formulario: {e}")
            return None

    def extract_data(self, selector, attribute=None):
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

            # Extraer con JavaScript
            table_data = self.page.evaluate(f"""
                () => {{
                    const table = document.querySelector('{table_selector}');
                    if (!table) return [];

                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    return rows.map(row => {{
                        const cells = Array.from(row.querySelectorAll('th, td'));
                        const anchors = Array.from(row.querySelectorAll('td a[target="_blank"]'));
                        const allCells = cells.map(cell => cell.innerText.trim());
                        const anchorHrefs = anchors.map(a => a.href);
                        return {{'cells': allCells, 'anchors': anchorHrefs }};
                    }});
                }}
            """)
            # anchors = self.extract_data("table tr td a[target='_blank'], href")
            titles = self.extract_data("th strong")
            all_text = self.get_all_text()

            return table_data, titles, all_text

        except Exception as e:
            print(f"Error extrayendo tabla: {e}")
            return []

    def get_all_text(self):
        """Obtiene todo el texto visible de la página"""
        return self.page.evaluate("() => document.body.innerText")
