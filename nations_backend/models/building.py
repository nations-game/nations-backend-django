from django.db.models import (
    CharField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

class NationBuilding(Model):
    nation = ForeignKey("Nation", on_delete=CASCADE, related_name="buildings")
    building_type = CharField(max_length=100)

    level = IntegerField(default=1)