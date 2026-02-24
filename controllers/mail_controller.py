from models import MailModel

class MailController():
    def __init__(self, model: MailModel) -> None:
        self.model = model

    def send(self):
        return self.model.send()
