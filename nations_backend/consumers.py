import json
import urllib

from channels.generic.websocket import WebsocketConsumer
from .models import User, Nation
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


class NationUpdateConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        params = urllib.parse.parse_qs(self.scope['query_string'].decode('utf8'))
        try:
            token = params.get('sessionid', (None,))[0]
            session = Session.objects.get(session_key=token)
            session = Session.objects.get(session_key=session)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)

            self.scope["user"] = user                    
        
        except:
            self.close()
            return

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
