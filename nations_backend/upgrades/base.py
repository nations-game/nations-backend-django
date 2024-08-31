from ..util import Commodities
from typing import List, Tuple
from enum import Enum

class BaseUpgrade:
    def __init__(
            self,
            name: str,
            description: str,
            base_cost: List[Tuple[Commodities, int]]
        ):
        self.name = name
        self.description = description
        self.base_cost = base_cost

        self.id = self.name.lower().replace(" ", "_")

    def __str__(self) -> str: return self.name

    def get_cost(self, level: int) -> List[Tuple[Commodities, int]]:
        cost = self.base_cost
        for commodity, quantity in cost:
            quantity *= level
        return cost
    
    def get_cost_dict(self, level: int) -> dict:
        cost_values = []
        for commodity, quantity in self.base_cost:
            cost_values.append({
                "commodity": commodity.value,
                "quantity": quantity * (1 + ((level) * 0.1))
            })

        return cost_values

    def to_dict(self, level: int = 1) -> dict:
        cost_values = self.get_cost_dict(level=level)

        return {
            "id": self.id,
            "name":  self.name,
            "description": self.description,
            "cost": cost_values,
            "level": level
        }

