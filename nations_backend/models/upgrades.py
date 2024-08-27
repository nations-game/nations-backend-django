from django.db.models import (
    CharField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

class NationUpgrade(Model):
    nation = ForeignKey("Nation", on_delete=CASCADE, related_name="upgrades")
    upgrade_type = CharField(max_length=100)
    level = IntegerField(default=1)