from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CharField, 
    FloatField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)
from ..military import unit_manager

class NationDivision(Model):
    nation = ForeignKey("Nation", on_delete=CASCADE, related_name="divisions")
    name = CharField(max_length=24)

    def get_units(self):
        return DivisionUnit.objects.filter(division=self).all()
    
    def to_dict(self) -> dict:
        units_list = []
        for unit in self.get_units():
            units_list.append(unit.to_dict())

        return {
            "name": self.name,
            "nation": self.nation.id,
            "units": units_list
        }

class DivisionUnit(Model):
    division = ForeignKey("NationDivision", on_delete=CASCADE, related_name="units")
    unit_type = CharField(max_length=100)
    health = IntegerField()

    def to_dict(self) -> dict:
        unit_type_data = unit_manager.get_unit_by_id(self.unit_type)
        data = unit_type_data.__dict__()
        data.update({
            "health": self.health,
            "division": self.division.id
        })