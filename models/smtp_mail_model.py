import json
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

import certifi
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
FILENAME_ESTADO = BASE_DIR / "form_results_estado.json"
FILENAME_TENDIOS = BASE_DIR / "form_results_tendios.json"


class SmtpMailModel:
    def __init__(self) -> None:
        self._smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self._smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self._smtp_user = os.getenv("SMTP_USER", "")
        self._smtp_password = os.getenv("SMTP_PASSWORD", "")
        self._from_email = os.getenv("FROM_EMAIL", self._smtp_user)
        self._to_email = os.getenv("TO_EMAIL", "")
        self._template_name = os.getenv("EMAIL_TEMPLATE", "email_template.html")

    @staticmethod
    def _format_item(item) -> dict:
        if not isinstance(item, dict):
            return {}
        org = item.get("contractingOrganization") or {}
        if isinstance(org, str):
            org = {"name": org}
        return {
            "id": item.get("id", ""),
            "expedient": item.get("expedient", ""),
            "name": item.get("name", item.get("title", "Sin título")),
            "budgetNoTaxes": item.get("budgetNoTaxes", item.get("budget", item.get("amount", 0))),
            "status": item.get("status", ""),
            "location": item.get("location", item.get("placeOfPerformance", "")),
            "contractingOrganization": {
                "name": org.get("name") or item.get("organizationName", item.get("entityName", ""))
            },
            "numLots": item.get("numLots", 0),
            "expedientPublishedAt": item.get("expedientPublishedAt", item.get("publishedAt", "")),
            "expedientSubmissionDeadline": item.get("expedientSubmissionDeadline", item.get("submissionDeadline", "")),
            "linkUrl": item.get("linkUrl", item.get("sourceUrl", "")),
        }

    def _load_data(self) -> tuple:
        estado_raw: list = []
        tendios_raw: list = []
        
        if FILENAME_ESTADO.exists():
            with open(FILENAME_ESTADO, encoding="utf-8") as f:
                estado_raw = json.load(f)
        
        if FILENAME_TENDIOS.exists():
            with open(FILENAME_TENDIOS, encoding="utf-8") as f:
                tendios_raw = json.load(f)

        estado_raw_items = estado_raw if isinstance(estado_raw, list) else estado_raw.get("data", [])
        tendios_raw_items = tendios_raw if isinstance(tendios_raw, list) else tendios_raw.get("data", [])

        def _normalize(raw_items):
            if not isinstance(raw_items, list):
                print(f"[WARN] datos no es una lista: {type(raw_items).__name__}")
                return []
            result = []
            for i, item in enumerate(raw_items):
                if isinstance(item, dict):
                    result.append(self._format_item(item))
                else:
                    print(f"[WARN] item {i} ignorado: {type(item).__name__}")
            return result

        return _normalize(estado_raw_items), _normalize(tendios_raw_items)

    def _render_template(self, estado_items: list[dict], tendios_items: list[dict]) -> str:
        env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
        template = env.get_template(self._template_name)
        return template.render(data=[estado_items, tendios_items])

    def send(self) -> dict:
        estado_items, tendios_items = self._load_data()
        total = len(estado_items) + len(tendios_items)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Actualització de Licitacions"
        msg["From"] = self._from_email
        msg["To"] = self._to_email

        html = self._render_template(estado_items, tendios_items)
        msg.attach(MIMEText(html, "html"))

        context = ssl.create_default_context(cafile=certifi.where())
        with smtplib.SMTP(self._smtp_host, self._smtp_port) as server:
            server.starttls(context=context)
            server.login(self._smtp_user, self._smtp_password)
            server.sendmail(self._from_email, self._to_email, msg.as_string())

        return {"status": "sent", "to": self._to_email, "items": total}
