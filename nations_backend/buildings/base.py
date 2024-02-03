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