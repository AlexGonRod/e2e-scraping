from typing import Protocol, Optional, Any
from pydantic import BaseModel

class MailData(BaseModel):
    sender: str = ""
    to: str = ""
    body: Optional[str] = ""
    options: Optional[dict[str,Any]] = {}

class MailModel(Protocol):
    def send(self) -> dict:
        ...
