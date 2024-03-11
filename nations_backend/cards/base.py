from typing import List, Tuple
from enum import Enum
from ..models import User

class Commodities(Enum):
    MONEY = "money"
    FOOD = "food"
    POWER = "power"
    BUILDING_MATERIALS = "building_materials"
    METAL = "metal"
    CONSUMER_GOODS = "consumer_goods"

class BaseCard:
    def __init__(
            self,
            name: str,
            description: str,
            cost: List[Tuple[Commodities, int]],
            category: str
        ):
        self.name = name
        self.description = description
        self.cost = cost
        self.category = category

        self.id = self.name.lower().replace(" ", "_")

    def on_use_card(self, user_invoked: User) -> None: pass

    def __str__(self) -> str: return self.name

    def __dict__(self) -> dict:
        cost_values = []

        for commodity, quantity in self.cost:
            cost_values.append({
                "commodity": commodity.value,
                "quantity": quantity
            })

        return {
            "id": self.id,
            "name":  self.name,
            "description": self.description,
            "cost": cost_values,
            "category": self.category
        }

