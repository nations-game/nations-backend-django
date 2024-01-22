from enum import Enum

from django.db.models import (
    CharField, 
    FloatField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)


class Nation(Model):
    name = CharField(max_length=24)
    system = IntegerField() # 0 = capitalism, 1 = socialism, 2 = dictatorship
    population = IntegerField()
    happiness = IntegerField() # min 0, max 100
    flag = CharField(max_length=200) # link to flag, will be implemented later
    
    # Commodities
    money = IntegerField(default=100_000)
    food = IntegerField(default=100_000)
    power = IntegerField(default=10_000)
    building_materials = IntegerField(default=1_000)
    metal = IntegerField(default=1_000)
    consumer_goods = IntegerField(default=10_000)

    # Info for ticking
    tax_rate = FloatField(default=1.0)

    # Leader info
    leader = ForeignKey("User", on_delete=CASCADE)

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "system": self.system,
            "leader_id": self.leader_id,

            # Commodities
            "money": self.money,
            "food": self.food,
            "power": self.power,
            "building_materials": self.building_materials,
            "metal": self.metal
        }


class NationSystem(Enum):
    CAPITALISM = 0
    SOCIALISM = 1
    DICTATORSHIP = 2