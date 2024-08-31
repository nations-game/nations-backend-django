from ..factories import Commodities

class BaseBuilding:
    def __init__(
            self, 
            name: str,
            description: str,
            max_level: int,
            cost: list[tuple[Commodities, int]]
        ) -> None:

        self.name = name
        self.description = description
        self.max_level = max_level
        self.cost = cost

        self.id = self.name.lower().replace(" ", "_")
        # self.cost.append((Commodities.UNUSED_LAND, 1))

    def get_upgrade_cost(self, current_level: int) -> list[tuple[Commodities, int]]:
        multiplier = 1 + (current_level * 0.1)
        new_cost = self.cost
        
        for commodity, quantity in new_cost:
            quantity *= multiplier

        return new_cost

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
            "max_level": self.max_level,
            "cost": cost_values if len(cost_values) > 0 else "free"
        }