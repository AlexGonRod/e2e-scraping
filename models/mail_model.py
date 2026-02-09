import os
from typing import Optional
from pydantic import BaseModel
import mailtrap as mt
from dotenv import load_dotenv

class MailData(BaseModel):
    sender: str = ""
    to: str = ""
    topic: str = ""
    body: Optional[str] = ""
    options: Optional[dict[str,str]] = {}

def get_client() -> mt.MailtrapClient:
    try:
        client = mt.MailtrapClient(token="5a43db29099bfa922d7db24cca664023")
        return client
    except Exception as e:
        print(f"Error creating Mailtrap client: {e}")
        raise e

class MailTrapModel:
    load_dotenv()
    def __init__(self) -> None:
        self._token = os.getenv("MAIL_API_KEY") or ""
        self._account_id = os.getenv("MAIL_ACCOUNT_ID")
        self._template_id = os.getenv("MAIL_TEMPLATE_ID") or ""

    def set_email(self) -> mt.Mail:
        # mail = mt.MailFromTemplate(
        #     sender=mt.Address(email=mail_options["sender"], name=mail_options["sender"]),
        #     to=[mt.Address(email=mail_options["to"])],
        #     template_uuid = os.getenv("MAIL_TEMPLATE_ID"),
        #     template_variables={
        #         "name": mail_options["options"]["name"] or "Rocio",
        #         # "status": self.mail_data["options"]["status"],
        #         # "budgetNoTaxes": self.mail_data["options"]["budgetNoTaxes"],
        #         # "expedientPublishedAt": self.mail_data["options"]["expedientPublishedAt"],
        #         # "contractingOrganization": self.mail_data["options"]["contractingOrganization"]["name"],
        #     }
        # )

        return mt.MailFromTemplate(
            sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
            to=[mt.Address(email="alexgonrod83@gmail.com")],
            template_uuid = os.getenv("MAIL_TEMPLATE_ID"),
            template_variables={
                "name":  "Rocio",
                # "status": self.mail_data["options"]["status"],
                # "budgetNoTaxes": self.mail_data["options"]["budgetNoTaxes"],
                # "expedientPublishedAt": self.mail_data["options"]["expedientPublishedAt"],
                # "contractingOrganization": self.mail_data["options"]["contractingOrganization"]["name"],
            }
        )

    def send(self) -> mt.SEND_ENDPOINT_RESPONSE:

        client = get_client()
        mail = self.set_email()
        response = client.send(mail)
        return response

