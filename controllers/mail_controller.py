
class MailController():
    def __init__(self, model) -> None:
        self.model = model

    def send(self):
        return self.model.send()
