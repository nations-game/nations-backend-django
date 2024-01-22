from django.db import models
from enum import Enum

class User(models.Model):
    __tablename__  = "users"
    # Basic account info
    username = models.CharField(max_length=24)
    email = models.CharField(max_length=100)

    # Password info
    hashed_password = models.CharField()
    salted_password = models.CharField()

    # Nation info
    nation = models.ForeignKey("Nation", on_delete=models.CASCADE)

    def __dict__(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "nation_id": self.nation_id
        }

class Nation(models.Model):
    name = models.CharField(max_length=24)
    system = models.IntegerField() # 0 = capitalism, 1 = socialism, 2 = dictatorship
    population = models.IntegerField()
    happiness = models.IntegerField() # min 0, max 100
    flag = models.CharField(max_length=200) # link to flag, will be implemented later
    
    # Commodities
    money = models.IntegerField(default=100_000)
    food = models.IntegerField(default=100_000)
    power = models.IntegerField(default=10_000)
    building_materials = models.IntegerField(default=1_000)
    metal = models.IntegerField(default=1_000)
    consumer_goods = models.IntegerField(default=10_000)

    # Info for ticking
    tax_rate = models.FloatField(default=1.0)

    # Leader info
    leader = models.ForeignKey(User, on_delete=models.CASCADE)

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

class FactoryType(models.Model):
    name = models.CharField(max_length=24)
    commodity = models.CharField(max_length=24)
    production = models.IntegerField(default=5)
    max_level = models.IntegerField(default=5)
    current_level = models.IntegerField(default=1)

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "commodity": self.commodity,
            "production": self.production,
            "max_level": self.max_level,
            "current_level": self.current_level
        }
    
class NationFactory(models.Model):
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    factory_type = models.ForeignKey(FactoryType, on_delete=models.CASCADE)