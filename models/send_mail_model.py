import os
import mailtrap as mt
from dotenv import load_dotenv
from models import MailData
from services import format_date

mail_options = MailData(
    sender = "alexgonrod83@gmail.com",
    to = "alexgonrod83@gmail.com",
    options = {
        "expedient": "GA08-26",
        "budgetNoTaxes": "100.000€",
        "expedientPublishedAt": "2026-02-16T23:00:00.000Z",
        "expedientSubmissionDeadline": "2026-02-24T13:00:00.000Z",
        "contractingOrganization": {
            "id": "6332f339015d7b5bc6170580",
            "name": "Forestal Catalana, SA"
        },
        }
)

def get_client() -> mt.MailtrapClient:
    try:
        client = mt.MailtrapClient(token="5a43db29099bfa922d7db24cca664023", sandbox=True, inbox_id="4365787")
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
                "expedient": mail_options.options.get("expedient", ""),
                "dateAt": format_date(mail_options.options.get("expedientPublishedAt", "")),
                "dateTo": format_date(mail_options.options.get("expedientSubmissionDeadline", "")),
                "budget": mail_options.options.get("budgetNoTaxes", ""),
                "id": mail_options.options.get("contractingOrganization", {}).get("name", ""),
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
