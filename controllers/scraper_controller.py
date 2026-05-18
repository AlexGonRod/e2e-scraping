
class ScraperController():
    def __init__(self, model) -> None:
        self.model = model

    async def scrape(self) -> dict:
        return await self.model.get()
