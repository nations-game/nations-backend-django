from django.db.models import (
    CharField, 
    FloatField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

class FactoryType(Model):
    name = CharField(max_length=24, unique=True)
    commodity = CharField(max_length=24)
    production = IntegerField(default=5)
    max_level = IntegerField(default=5)
    current_level = IntegerField(default=1)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "commodity": self.commodity,
            "production": self.production,
            "max_level": self.max_level,
            "current_level": self.current_level
        }


class NationFactory(Model):
    nation = ForeignKey("Nation", on_delete=CASCADE, related_name="factories")
    factory_type = ForeignKey(FactoryType, on_delete=CASCADE)
    production_resources = ForeignKey(int, on_delete=CASCADE) # Not sure what this does (yea i'm pretty stupid)