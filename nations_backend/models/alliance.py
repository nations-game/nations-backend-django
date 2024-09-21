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

    # If I don't set it to nullable I have to delete all the migrations
    owner = ForeignKey("Nation", on_delete=CASCADE, related_name="alliance_owner", blank=True, null=True)

    # Alliance shout
    shout = ForeignKey("AllianceShout", on_delete=CASCADE, blank=True, null=True)

    def get_member_count(self):
        return AllianceMember.objects.filter(alliance=self).count()
    
    def get_pending_requests(self):
        return AllianceRequest.objects.filter(alliance=self).all()
    
    def get_alliance_members(self):
        return AllianceMember.objects.filter(alliance=self).all()
    
    def get_alliance_administrators(self):
        return AllianceMember.objects.filter(alliance=self, role=1).all()
    
    def get_alliance_owner(self):
        return AllianceMember.objects.filter(alliance=self, role=2).first()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "status": "public" if self.public else "private",
            "member_count": self.get_member_count(),
            "owner_nation_id": self.owner.id,
            "shout": self.shout.to_dict() if self.shout is not None else "empty"
        }

class AllianceShout(Model):
    shouting_nation = ForeignKey("Nation", on_delete=CASCADE)
    text = CharField(max_length=500)

    def to_dict(self) -> dict:
        return {
            "nation": self.shouting_nation.id,
            "text": self.text
        }

class AllianceRequest(Model):
    timestamp = IntegerField()

    requesting_nation = ForeignKey("Nation", on_delete=CASCADE)
    alliance = ForeignKey("Alliance", on_delete=CASCADE)

class AllianceMember(Model):
    nation = ForeignKey("Nation", on_delete=CASCADE, related_name="alliance")
    alliance = ForeignKey("Alliance", on_delete=CASCADE)
    role = IntegerField(default=0) # 0 = member, 1 = admin, 2 = owner

class AllianceAllyRequest(Model):
    timestamp = IntegerField()

    requesting_alliance = ForeignKey("Alliance", on_delete=CASCADE, related_name="requester")
    alliance = ForeignKey("Alliance", on_delete=CASCADE)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "requester": self.requesting_alliance.to_dict()
        }

class AllianceAlly(Model):
    requester = ForeignKey("Alliance", on_delete=CASCADE)
    acceptor = ForeignKey("Alliance", on_delete=CASCADE, related_name="accepted_allies")

class AllianceEnemy(Model):
    aggressor = ForeignKey("Alliance", on_delete=CASCADE)
    enemy = ForeignKey("Alliance", on_delete=CASCADE, related_name="enemies")

class AllianceRole:
    MEMBER = 0
    ADMIN = 1
    OWNER = 2