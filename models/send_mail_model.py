import os
import mailtrap as mt
from dotenv import load_dotenv
from models import MailData

load_dotenv()

mail_options = MailData(
    sender = "alexgonrod83@gmail.com",
    to = "alexgonrod83@gmail.com",
    options = {
      "id": "019c7b3b-d2cf-73ee-be27-1d184fbce10f",
      "expedient": "2025_0169",
      "name": "Alojamiento y manutención de animales que exceden la capacidad del centro municipal de protección animal",
      "budgetNoTaxes": 58400,
      "status": "Publicada",
      "location": "Murcia, Área Metropolitana de Murcia, Región de Murcia, España",
      "contractingOrganization": {
        "id": "632f4d5290a1f608455391c7",
        "name": "Junta de Gobierno del Ayuntamiento de Murcia"
      },
      "numLots": 0,
      "expedientPublishedAt": "2026-02-20T13:23:57.000Z",
      "expedientSubmissionDeadline": "2026-03-06T22:59:00.000Z"
    },
)

def get_client(token, inbox_id) -> mt.MailtrapClient:
    try:
        client = mt.MailtrapClient(token, inbox_id=inbox_id, sandbox=True)
        if not client:
            raise RuntimeError("No se pudo crear el cliente de Mailtrap")

        return client

    except Exception as e:
        print(f"Error creating Mailtrap client: {e}")
        raise e

def set_email() -> mt.MailFromTemplate:

    try:
        result = mt.MailFromTemplate(
            sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
            to=[mt.Address(email="alexgonrod83@gmail.com")],
            template_uuid = os.getenv("MAIL_TEMPLATE_ID") or "",
            template_variables={
                'data': [mail_options.options, mail_options.options]
            }
        )
        if not result:
            raise RuntimeError("No se pudo crear el correo electrónico a partir de la plantilla")

        return result

    except Exception as e:
        print(f"Error creating email from template: {e}")
        raise e


class MailTrapModel():
    load_dotenv()
    def __init__(self) -> None:
        self._token = os.getenv("MAIL_TOKEN") or ""
        self._inbox_id = os.getenv("MAIL_INBOX_ID") or ""
        self._account_id = os.getenv("MAIL_ACCOUNT_ID")
        self._template_id = os.getenv("MAIL_TEMPLATE_ID") or ""

    def send(self) -> mt.SEND_ENDPOINT_RESPONSE:
        try:
            client = get_client(self._token, self._inbox_id)
            template = set_email()
            email = client.send(template)
            return email

        except Exception as e:
            raise RuntimeError(f"Error sending email: {e}") from e
