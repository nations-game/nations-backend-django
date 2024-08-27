from ..util import Commodities
from typing import List, Tuple
from enum import Enum

class BaseFactory:
    def __init__(
            self,
            name: str,
            description: str,
            input: List[Tuple[Commodities, int]],
            output: List[Tuple[Commodities, int]],
            cost: List[Tuple[Commodities, int]],
            category: str
        ):
        self.name = name
        self.description = description
        self.input = input
        self.output = output
        self.cost = cost
        self.category = category

        self.id = self.name.lower().replace(" ", "_")

    def __str__(self) -> str: return self.name

    def __dict__(self) -> dict:
        input_values = []
        output_values = []
        cost_values = []
        
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
            "input": input_values,
            "output": output_values,
            "category": self.category
        }

