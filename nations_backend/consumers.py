import json

from channels.generic.websocket import WebsocketConsumer
from .models import User, Nation
from asgiref.sync import async_to_sync

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
        async_to_sync(self.channel_layer.group_add)("nation_updates_group", self.channel_name) 
        # nation_updated.connect(self.on_nation_updated)

    def nation_updated(self, event):
        nation = event["nation"]
        self.send(text_data=json.dumps(nation.to_dict()))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("nation_updates_group", self.channel_name)
        pass

    def receive(self, text_data):
        pass
