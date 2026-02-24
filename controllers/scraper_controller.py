
class ScraperController():
    def __init__(self, model) -> None:
        self.model = model

    def scrape(self) -> dict:
        return self.model.get()
