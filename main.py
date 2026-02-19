import json
from typing import List
from models import PlaywrightModel as Model, tendios_model, MailTrapModel
from controllers import MailController, PlaywrightController
from services import save_data_to_json

URL = "https://contrataciondelestado.es/wps/portal/plataforma/buscadores/busqueda/!ut/p/z1/jY9LT8MwEIR_C4dcvVvnARzTPF0VNRCcNL5UbgnIKK5DHvx-DOq1oXub1TczuyBgD-Isv9WHnJQ5y87qRgQHL9lFUZpTfCjdGOk25jzIrcx8qP8A3428alMVQckyRJan8ZavfMxoAOIWP16ZEG_zLwBiOb4GsVxBL8DSi_-VNPbI-0NYJc8he3Rxt36xFZvi6bXI6ArRg_I342Q0UUdN3uWpHUlvhqlrJ1KxpGYxNA5-jr2Dx3n8mts36WBqBj13clBmfdkRS0CvOd-jKrQO734AYHmecg!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/p0/IZ7_AVEQAI930OBRD02JPMTPG21004=CZ6_4EOCCFH208S3D02LDUU6HH20G5=LA0=Ecom.ibm.faces.portlet.VIEWID!QCPjspQCPbusquedaQCPFormularioBusqueda.jsp==/#Z7_AVEQAI930OBRD02JPMTPG21004"
cpvs: List[str] = ['15713000','15712000','35250000','44619300','45223600','80512000']
FILENAME = "form_results.json"

class GetFormData:
    def get(self) -> dict[str, str | list]:
        return {
                "[id='viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:menu1MAQ1']": 'ES',
                "[id='viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:cpvMultiple:codigoCpv']": [15712000, 15713000, 35250000, 44619300, 45223600, 80512000],
                "[id='viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:estadoLici']": 'PUB',
                "[id='viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1']": 'click',
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
        self.filename = FILENAME

    @save_data_to_json
    def save(self):
        return self.controller.extract_table("#myTablaBusquedaCustom")

class ScrapeWithForm():
    def __init__(self, loader: GetFormData, controller: ScraperModel, exporter: SaveDataToJSON):
        self.loader = loader
        self.controller = controller
        self.exporter = exporter

    def run(self) -> None:
        form_data = self.loader.get()
        controller = self.controller.scrape()
        html = controller.fill_form_and_scrape(URL, form_data)

        if html:
            self.exporter.save()

class FetchData():
    def __init__(self, controller):
        self.controller = controller
        self.filename = FILENAME

    @save_data_to_json
    def fetch(self) -> None:
        print("=== Llamada a API ===")
        return self.controller(cpvs_codes=cpvs)

class SendMail():
    def __init__(self, model: MailController):
        self.controller = model

    def execute(self):
        return self.controller.send_mail()


def main() -> None:
    tendios_controller = tendios_model
    tendios_data = FetchData(tendios_controller)
    if not tendios_data:
        with Model() as pr:
            loader = GetFormData()
            controller = ScraperModel(pr)
            model = controller.scrape()
            exporter = SaveDataToJSON(model)
            data = ScrapeWithForm(loader, controller, exporter)
            data.run()
    else:
        tendios_data.fetch()



    # model = MailTrapModel()
    # controller = MailController(model)
    # mail_response = controller.send_mail()
    # print(mail_response)


if __name__ == "__main__":
    main()
