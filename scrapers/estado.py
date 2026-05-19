import asyncio
from models import PlaywrightModel as Model
from controllers import PlaywrightController
from services import save_data_to_json

URL_LICITACIONES = "https://contrataciondelestado.es/wps/portal/plataforma/buscadores/busqueda/!ut/p/z1/jY9LT8MwEIR_C4dcvVvnARzTPF0VNRCcNL5UbgnIKK5DHvx-DOq1oXub1TczuyBgD-Isv9WHnJQ5y87qRgQHL9lFUZpTfCjdGOk25jzIrcx8qP8A3428alMVQckyRJan8ZavfMxoAOIWP16ZEG_zLwBiOb4GsVxBL8DSi_-VNPbI-0NYJc8he3Rxt36xFZvi6bXI6ArRg_I342Q0UUdN3uWpHUlvhqlrJ1KxpGYxNA5-jr2Dx3n8mts36WBqBj13clBmfdkRS0CvOd-jKrQO734AYHmecg!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/p0/IZ7_AVEQAI930OBRD02JPMTPG21004=CZ6_4EOCCFH208S3D02LDUU6HH20G5=LA0=Ecom.ibm.faces.portlet.VIEWID!QCPjspQCPbusquedaQCPFormularioBusqueda.jsp==/#Z7_AVEQAI930OBRD02JPMTPG21004"
URL_MENORES = "https://contrataciondelestado.es/wps/portal/plataforma/buscadores/busqueda/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8ziTVz9nZ3dPIwMLIKNXQyMfFxCQ808gFx3U_1wsAJTY2eTMK-wALNgT3cDA08PNxefUENTA3cjM_0oYvQb4ACOBsTpx6MgCr_x4fpR-K0wgirA50VClhTkhoZGGGR6AgA3hHJw/dz/d5/L2dBISEvZ0FBIS9nQSEh/p0/IZ7_AVEQAI930OBRD02JPMTPG21004=CZ6_4EOCCFH208S3D02LDUU6HH20G5=LA0=Ecom.ibm.faces.portlet.VIEWID!QCPjspQCPbusquedaQCPMainBusqueda.jsp==/#Z7_AVEQAI930OBRD02JPMTPG21004"
FILENAME_ESTADO = "form_results_estado.json"


class GetFormData:
    def get(self) -> dict[str, str | list]:
        return {
            "[id='viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:menu1MAQ1']": "ES",
            "[id='viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:cpvMultiple:codigoCpv']": [
                24600000,
                38546000,
                39500000,
                44423000,
                44619300,
                80512000,
            ],
            "[id='viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:estadoLici']": "PUB",
            "[id='viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1']": "click",
        }


class ScraperModel:
    def __init__(self, model: Model) -> None:
        self.model = model

    def scrape(self) -> PlaywrightController:
        if self.model.page is None:
            raise RuntimeError("No se pudo inicializar la página de Playwright")
        return PlaywrightController(self.model.page)


class SaveDataToJSON:
    def __init__(self, controller: PlaywrightController) -> None:
        self.controller = controller
        self.filename = FILENAME_ESTADO

    @save_data_to_json
    def save(self):
        print("=== Scraping PW ===")
        return self.controller.extract_table("#myTablaBusquedaCustom")


class ScrapeWithForm:
    def __init__(
        self, loader: GetFormData, controller: ScraperModel, exporter: SaveDataToJSON
    ):
        self.loader = loader
        self.controller = controller
        self.exporter = exporter

    def run(self) -> None:
        form_data = self.loader.get()
        controller = self.controller.scrape()
        html = controller.fill_form_and_scrape(URL_LICITACIONES, form_data)
        if html:
            self.exporter.save()


def _sync_scrape():
    with Model() as pr:
        loader = GetFormData()
        controller = ScraperModel(pr)
        model = controller.scrape()
        exporter = SaveDataToJSON(model)
        data = ScrapeWithForm(loader, controller, exporter)
        data.run()


async def scrapePW():
    print("=== Scrapping ===")
    await asyncio.to_thread(_sync_scrape)
