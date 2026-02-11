import os
import mailtrap as mt
from dotenv import load_dotenv
from models import MailData

mail_options = MailData(
    sender = "alexgonrod83@gmail.com",
    to = "alexgonrod83@gmail.com",
    options = {
        "name": "Rocío",
        "status": "Publicada",
        "budgetNoTaxes": "100.000€",
        "expedientPublishedAt": "2024-06-01",
        "contractingOrganization": {
            "name": "Ayuntamiento de Madrid"
            }
        }
)

def get_client() -> mt.MailtrapClient:
    try:
        client = mt.MailtrapClient(token="5a43db29099bfa922d7db24cca664023")
        return client
    except Exception as e:
        print(f"Error creating Mailtrap client: {e}")
        raise e

class MailTrapModel():
    load_dotenv()
    def __init__(self) -> None:
        self._token = os.getenv("MAIL_API_KEY") or ""
        self._account_id = os.getenv("MAIL_ACCOUNT_ID")
        self._template_id = os.getenv("MAIL_TEMPLATE_ID") or ""

    def set_email(self) -> mt.MailFromTemplate:

        return mt.MailFromTemplate(
            sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
            to=[mt.Address(email="alexgonrod83@gmail.com")],
            template_uuid = os.getenv("MAIL_TEMPLATE_ID") or "",
            template_variables={
                "name": mail_options.sender or "Rocio",
                # "status": mail_data.options.status,
                # "budgetNoTaxes": mail_data.options.budgetNoTaxes,
                # "expedientPublishedAt": mail_data.options.expedientPublishedAt,
                # "contractingOrganization": mail_data.options.contractingOrganization.name,
            }
        )

    def send(self) -> mt.SEND_ENDPOINT_RESPONSE:
        try:
            client = get_client()
            template = self.set_email()
            email = client.send(template)
            return email

        except Exception as e:
            raise RuntimeError(f"Error sending email: {e}") from e
