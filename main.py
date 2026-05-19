import asyncio
from models import SmtpMailModel
from controllers import MailController
from scrapers import fetchTendios, scrapePW


class SendMail:
    def __init__(self, controller: MailController) -> None:
        self.controller = controller

    def send(self) -> dict:
        return self.controller.send()


async def main() -> None:
    await fetchTendios()
    await scrapePW()

    print("=== Sending mail ===")
    mail_model = SmtpMailModel()
    mail_controller = MailController(mail_model)
    SendMail(mail_controller).send()
    print("=== mail sent to: " + mail_model._to_email + " ===")


if __name__ == "__main__":
    asyncio.run(main())
