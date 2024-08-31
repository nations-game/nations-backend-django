import json

from channels.generic.websocket import WebsocketConsumer
from .models import User, Nation


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))


class NationUpdateConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user: User = self.scope["user"]
        self.nation: Nation = self.user.nation
        print(self.user.to_dict())
        print(self.nation.to_dict())

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass
