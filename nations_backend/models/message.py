from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    BooleanField,
    CharField,
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

class Message(Model):
    sender = ForeignKey("User", on_delete=CASCADE, related_name="sender")
    recipient = ForeignKey("User", on_delete=CASCADE, related_name="recipient")

    subject = CharField(max_length=512)
    text = CharField(max_length=2048)

    timestamp = IntegerField()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sender": self.sender.id if self.sender else "System",
            "subject": self.subject,
            "text": self.text,
            "timestamp": self.timestamp
        }
    
    def to_short_dict(self) -> dict:
        return {
            "id": self.id,
            "sender": self.sender.id if self.sender else "System",
            "subject": self.subject,
            "timestamp": self.timestamp
        }
