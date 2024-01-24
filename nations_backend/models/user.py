from django.contrib.auth.models import AbstractUser
from django.db.models import (
    EmailField,
    CharField, 
    ForeignKey, 
    CASCADE
)

class User(AbstractUser):
    # Nation info
    nation = ForeignKey("Nation", on_delete=CASCADE, blank=True, null=True)

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "nation_id": self.nation_id
        }