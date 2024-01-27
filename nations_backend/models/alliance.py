from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

class Alliance(Model):
    nation_owner = ForeignKey("Nation", on_delete=CASCADE, related_name="alliance")
    
    def get_pending_requests(self):
        return AllianceRequest.objects.filter(alliance=self).all()

class AllianceRequest(Model):
    timestamp = IntegerField()

    requester = ForeignKey("User", on_delete=CASCADE)
    alliance = ForeignKey("Alliance", on_delete=CASCADE)