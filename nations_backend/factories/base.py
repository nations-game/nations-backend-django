from typing import List, Tuple
from enum import Enum

class Commodities(Enum):
    MONEY = "money"
    FOOD = "food"
    POWER = "power"
    BUILDING_MATERIALS = "building_materials"
    METAL = "metal"
    CONSUMER_GOODS = "consumer_goods"

class BaseFactory:
    def __init__(
            self,
            name: str,
            description: str,
            input: List[Tuple[Commodities, int]],
            output: List[Tuple[Commodities, int]],
            cost: List[Tuple[Commodities, int]]
        ):
        self.name = name
        self.description = description
        self.input = input
        self.output = output
        self.cost = cost

        self.id = self.name.lower().replace(" ", "_")

    def __str__(self) -> str: return self.name

    def __dict__(self) -> dict:
        input_values = []
        output_values = []
        
        for commodity, quantity in self.input:
            input_values.append({
                "commodity": commodity.value,
                "quantity": quantity
            })

        for commodity, quantity in self.output:
            output_values.append({
                "commodity": commodity.value,
                "quantity": quantity
            })
        return {
            "id": self.id,
            "name":  self.name,
            "description": self.description,
            "input": input_values,
            "output": output_values
        }

