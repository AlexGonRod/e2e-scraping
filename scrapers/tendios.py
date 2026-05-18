from models import TendiosModel
from controllers import ScraperController
from services import save_data_to_json

FILENAME_TENDIOS = "form_results_tendios.json"


class FetchDataTendios:
    def __init__(self, controller: ScraperController) -> None:
        self.controller = controller
        self.filename = FILENAME_TENDIOS

    @save_data_to_json
    async def fetch(self) -> dict:
        print("=== Calling Tendios API ===")
        return await self.controller.scrape()


async def fetchTendios():
    scraper_model = TendiosModel()
    scraper_controller = ScraperController(scraper_model)
    tendios_data = await FetchDataTendios(scraper_controller).fetch()
    return tendios_data
