from ..util import Commodities
from typing import List, Tuple
from enum import Enum

class UnitCategories(Enum):
    INFANTRY = "infantry"
    ARMORED = "armored"
    AIR = "air"
    SPECIAL = "special"

class UnitType:
    def __init__(self, 
                name: str, 
                max_health: int, 
                att: int, 
                defense: int,
                recruit_cost: List[Tuple[Commodities, int]],
                upkeep: List[Tuple[Commodities, int]],
                category: UnitCategories
        ) -> None:
        self.name = name
        self.max_health = max_health
        self.att = att
        self.defense = defense
        self.recruit_cost = recruit_cost
        self.upkeep = upkeep
        self.category = category

        self.id = name.lower().replace(" ", "_")
        pass

    def __str__(self) -> str: return self.name

    def __dict__(self) -> dict:
        recruit_values = []
        upkeep_values = []
        
        for commodity, quantity in self.recruit_cost:
            recruit_values.append({
                "commodity": commodity.value,
                "quantity": quantity
            })

        for commodity, quantity in self.upkeep:
            upkeep_values.append({
                "commodity": commodity.value,
                "quantity": quantity
            })
            
        return {
            "id": self.id,
            "name":  self.name,
            "category": self.category.value,
            "cost": recruit_values,
            "upkeep": upkeep_values,
            "max_health": self.max_health,
            "att": self.att,
            "def": self.defense
        }

