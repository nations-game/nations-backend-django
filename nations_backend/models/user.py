from django.contrib.auth.models import User as DjangoUser
from django.db.models import (
    CharField, 
    ForeignKey, 
    CASCADE
)


class User(DjangoUser):    
    # Nation info
    nation = ForeignKey("Nation", on_delete=CASCADE)

    def __dict__(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "nation_id": self.nation_id
        }