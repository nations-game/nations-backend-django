import json
import urllib

from channels.generic.websocket import WebsocketConsumer
from .models import User, Nation, Notification
from asgiref.sync import async_to_sync
from django.contrib.sessions.models import Session

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))


class NationMessagesConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        params = urllib.parse.parse_qs(self.scope["query_string"].decode("utf8"))
        try:
            token = params.get("sessionid", (None,))[0]
            session = Session.objects.get(session_key=token)
            session = Session.objects.get(session_key=session)
            uid = session.get_decoded().get("_auth_user_id")
            user = User.objects.get(pk=uid)

            self.scope["user"] = user                    
        
        except:
            self.send(text_data="Unauthorized")
            self.close()
            return

        self.user: User = self.scope["user"]
        self.nation: Nation = self.user.nation
        self.send(text_data=json.dumps(self.user.to_dict()))
        print(f"{self.user.username} (ID {self.user.id}) connected to websocket")
        async_to_sync(self.channel_layer.group_add)("nation_updates_group", self.channel_name) 
        async_to_sync(self.channel_layer.group_add)("notifications_group", self.channel_name) 
        # nation_updated.connect(self.on_nation_updated)

    def nation_updated(self, event):
        nation: Nation = event["nation"]
        if nation.leader == self.user:
            self.send(text_data=json.dumps({ "action": "nationUpdated", "nation": nation.to_dict() }))

    def notification_received(self, event):
        notification: Notification = event["notification"]
        if notification.user == self.user:
            self.send(text_data=json.dumps({ "action": "notificationReceived", "notification": notification.to_dict() }))

    def disconnect(self, close_code):
        print(f"{self.user.username} (ID {self.user.id}) disconnected from websocket")
        async_to_sync(self.channel_layer.group_discard)("nation_updates_group", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)("notifications_group", self.channel_name) 
        pass

    def receive(self, text_data):
        pass
