from django.db.models import (
    CharField, 
    FloatField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

class NationFactory(Model):
    nation = ForeignKey("Nation", on_delete=CASCADE, related_name="factories")
    factory_type = CharField(max_length=100)
    produced_commodities = IntegerField(default=0) # Not sure what this does (yea i'm pretty stupid)