from playwright.sync_api import Page
from services import fill_form, extract_data, extract_table

class PlaywrightController:

    def __init__(self,page: Page):
        self.page = page

    def fill_form_and_scrape(self, url, form_selectors):
        return fill_form(self, url, form_selectors)

    def extract_data(self, selector, attribute=None):
        return extract_data(self, selector, attribute)

    def extract_table(self, table_selector="table"):
        """Extrae datos de una tabla HTML"""
        return extract_table(self, table_selector)

    def get_all_text(self):
        """Obtiene todo el texto visible de la página"""
        return self.page.evaluate("() => document.body.innerText")
