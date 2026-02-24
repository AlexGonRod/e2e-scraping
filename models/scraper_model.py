from typing import Protocol

class ScraperModel(Protocol):
    def get(self) -> dict:
        ...
