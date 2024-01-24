from enum import Enum

from django.db.models import (
    CharField, 
    FloatField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

from .factories import NationFactory

class Nation(Model):
    
    name = CharField(max_length=24)
    population = IntegerField(default=50_000)
    happiness = IntegerField(default=75) # min 0, max 100
    flag = CharField(max_length=200) # link to flag, will be implemented later

    SYSTEM_CHOICES = (
        (0, "Capitalism"),
        (1, "Socialism"),
        (2, "Dictatorship")
    )
    
    system = IntegerField(choices=SYSTEM_CHOICES) # 0 = capitalism, 1 = socialism, 2 = dictatorship
    
    # Commodities
    money = IntegerField(default=100_000)
    food = IntegerField(default=100_000)
    power = IntegerField(default=10_000)
    building_materials = IntegerField(default=10_000)
    metal = IntegerField(default=100)
    consumer_goods = IntegerField(default=10_000)

    # Info for ticking
    tax_rate = FloatField(default=1.0)

    # Leader info
    leader = ForeignKey("User", related_name="leader", on_delete=CASCADE)

    def to_dict(self):
        return {
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
    
    def get_factories(self):
        return NationFactory.objects.filter(nation=self).all()

class NationSystem(Enum):
    CAPITALISM = 0
    SOCIALISM = 1
    DICTATORSHIP = 2