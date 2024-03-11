from enum import Enum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CharField, 
    FloatField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

from .factories import NationFactory
from .building import NationBuilding
from .alliance import Alliance, AllianceMember

class Nation(Model):
    
    name = CharField(max_length=24)
    population = IntegerField(default=50_000)
    flag = CharField(max_length=200) # link to flag, will be implemented later

    happiness = IntegerField(default=5,
        validators=[
            MinValueValidator(-10),
            MaxValueValidator(10)
    ])

    SYSTEM_CHOICES = (
        (0, "Capitalism"),
        (1, "Socialism"),
        (2, "Dictatorship")
    )
    
    system = IntegerField(choices=SYSTEM_CHOICES) # 0 = capitalism, 1 = socialism, 2 = dictatorship
    
    # Commodities
    money = IntegerField(default=100_000)
    food = IntegerField(default=100_000)
    power = IntegerField(default=50_000)
    building_materials = IntegerField(default=50_000)
    metal = IntegerField(default=100)
    consumer_goods = IntegerField(default=10_000)

    # Info for ticking
    taxes_to_collect = IntegerField(default=0)

    # Leader info
    leader = ForeignKey("User", related_name="leader", on_delete=CASCADE)

    def to_dict(self):
        return {
            # basic info
            "name": self.name,
            "system": self.system,
            "leader_id": self.leader_id,

            # stats
            "population": self.population,
            "happiness": self.happiness,
            "pendingTaxes": self.taxes_to_collect,

            # Commodities
            "money": self.money,
            "food": self.food,
            "power": self.power,
            "buildingMaterials": self.building_materials,
            "metal": self.metal,
            "consumerGoods": self.consumer_goods
        }
    
    def get_factories(self):
        return NationFactory.objects.filter(nation=self).all()
    
    def get_buildings(self):
        return NationBuilding.objects.filter(nation=self).all()
    
    def has_building(self, building_id: str) -> bool:
        existing_building = NationBuilding.objects.filter(nation=self, building_type=building_id).first()
        return existing_building is not None
    
    def get_alliance(self) -> Alliance:
        alliance_member = AllianceMember.objects.filter(nation=self).first()
        
        if alliance_member != None:
            return alliance_member.alliance
        else: return None