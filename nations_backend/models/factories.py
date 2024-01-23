from django.db.models import (
    CharField, 
    FloatField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)


class FactoryType(Model):
    
    name = CharField(max_length=24)
    commodity = CharField(max_length=24)
    production = IntegerField(default=5)
    max_level = IntegerField(default=5)
    current_level = IntegerField(default=1)

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "commodity": self.commodity,
            "production": self.production,
            "max_level": self.max_level,
            "current_level": self.current_level
        }


class NationFactory(Model):
    nation = ForeignKey("Nation", on_delete=CASCADE)
    factory_type = ForeignKey(FactoryType, on_delete=CASCADE)