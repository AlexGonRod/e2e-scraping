import json
from typing import List
from models import PlaywrightModel as Model, tendios_model, MailTrapModel
from controllers import MailController, PlaywrightController

URL = "https://contrataciondelestado.es/wps/portal/plataforma/buscadores/busqueda/!ut/p/z1/jY9LT8MwEIR_C4dcvVvnARzTPF0VNRCcNL5UbgnIKK5DHvx-DOq1oXub1TczuyBgD-Isv9WHnJQ5y87qRgQHL9lFUZpTfCjdGOk25jzIrcx8qP8A3428alMVQckyRJan8ZavfMxoAOIWP16ZEG_zLwBiOb4GsVxBL8DSi_-VNPbI-0NYJc8he3Rxt36xFZvi6bXI6ArRg_I342Q0UUdN3uWpHUlvhqlrJ1KxpGYxNA5-jr2Dx3n8mts36WBqBj13clBmfdkRS0CvOd-jKrQO734AYHmecg!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/p0/IZ7_AVEQAI930OBRD02JPMTPG21004=CZ6_4EOCCFH208S3D02LDUU6HH20G5=LA0=Ecom.ibm.faces.portlet.VIEWID!QCPjspQCPbusquedaQCPFormularioBusqueda.jsp==/#Z7_AVEQAI930OBRD02JPMTPG21004"
cpvs: List[str] = ['15713000','15712000','35250000','44619300','45223600','80512000']

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

    def scrape(self) -> Controller:
        if self.model.page is None:
            raise RuntimeError("No se pudo inicializar la página de Playwright")

        return Controller(self.model.page)

class SaveHTML:
    def __init__(self, controller: Controller):
        self.controller = controller

    def save(self) -> None:
        with open("form_results.json", "w", encoding="utf-8") as f:
            results, titles, all_text = self.controller.extract_table("#myTablaBusquedaCustom")
            json.dump({
                'table': results,
                'titles': titles,
                'text': all_text[:1000]
            }, f, ensure_ascii=False, indent=2)

class ScrapeWithForm():
    def __init__(self, loader: GetFormData, controller: ScraperModel, exporter: SaveHTML):
        self.loader = loader
        self.controller = controller
        self.exporter = exporter

    def run(self) -> None:
        form_data = self.loader.get()
        controller = self.controller.scrape()
        print("=== Scraping directo ===")
        html = controller.fill_form_and_scrape(URL, form_data)

        if html:
            self.exporter.save()
            print("\nDatos guardados en form_results.json")

            # Mailmodel().send_mail()

class FetchData():
    def __init__(self, controller):
        self.controller = controller

    def fetch(self) -> None:
        print("=== Llamada a API ===")
        response = self.controller(cpvs_codes=cpvs)
        with open("api_results.json", "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=2)
        print("Datos guardados en api_results.json")

class SendMail():
    def __init__(self, model: MailController):
        self.controller = model

    def execute(self):
        return self.controller.send_mail()


def main() -> None:
    # loader = GetFormData()
    # with Model() as pr:
        # controller = ScraperModel(pr)
        # model = controller.scrape()
        # exporter = SaveHTML(model)
        # data = ScrapeWithForm(loader, controller, exporter)
        # data.run()
    data = FetchData(tendios_model)
    data.fetch()


    model = MailTrapModel()
    controller = MailController(model)
    mail_response = controller.send_mail()
    print(mail_response)


if __name__ == "__main__":
    main()
