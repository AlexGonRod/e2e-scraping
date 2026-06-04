from typing import Any, Optional, Protocol

from pydantic import BaseModel


class MailData(BaseModel):
    sender: str = ""
    to: str = ""
    subject: str = ""
    body: Optional[str] = ""
    options: dict[str,Any] = {}

class MailModel(Protocol):
    def send(self) -> dict:
        ...
