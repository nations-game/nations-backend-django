from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    BooleanField,
    CharField,
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

class Alliance(Model):
    name = CharField(max_length=24)
    icon = CharField(max_length=100) # path to image
    public = BooleanField(default=True)

    def get_member_count(self):
        members = self.get_alliance_members()
        return len(members)
    
    def get_pending_requests(self):
        return AllianceRequest.objects.filter(alliance=self).all()
    
    def get_alliance_members(self):
        return AllianceMember.objects.filter(alliance=self).all()
    
    def get_alliance_administrators(self):
        return AllianceMember.objects.filter(alliance=self, role=1).all()
    
    def get_alliance_owner(self):
        return AllianceMember.objects.filter(alliance=self, role=2).first()

class AllianceRequest(Model):
    timestamp = IntegerField()

    requesting_nation = ForeignKey("Nation", on_delete=CASCADE)
    alliance = ForeignKey("Alliance", on_delete=CASCADE)

class AllianceMember(Model):
    nation = ForeignKey("Nation", on_delete=CASCADE, related_name="alliance")
    alliance = ForeignKey("Alliance", on_delete=CASCADE)
    role = IntegerField(default=0) # 0 = member, 1 = admin, 2 = owner