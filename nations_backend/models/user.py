from django.contrib.auth.models import AbstractUser
from django.db.models import (
    ForeignKey, 
    CharField,
    IntegerField,
    BooleanField,
    CASCADE,
    Model
)

import time

class User(AbstractUser):
    # Nation info
    nation = ForeignKey("Nation", on_delete=CASCADE, blank=True, null=True)

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "nation_id": self.nation_id
        }
    
    def post_notification(self, title: str, details: str) -> "Notification":
        notification = Notification.objects.create(
            user=self,
            title=title,
            details=details,
            timestamp=time.time()
        )

        return notification
    
class Notification(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=250)
    details = CharField(max_length=500)
    timestamp = IntegerField()

    # 0 = displayed in notification widget,
    # 1 = banner display on dashboard, 
    # 2 = popup on dashboard and banner display
    urgency = IntegerField(default=0)

    # If the notification has been read/dismissed.
    read = BooleanField(default=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "receiving_user_id": self.user.id,
            "title": self.title,
            "details": self.details,
            "timestamp": self.timestamp,
            "urgency": self.urgency,
            "read": self.read
        }