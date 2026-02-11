from models import MailModel

class MailController():
    def __init__(self, model: MailModel) -> None:
        self.model = model

    def send_mail(self):
        return self.model.send()
