from ..base import BaseFactory, Commodities

class FoodFactories:
    def __init__(self, factory_manager) -> None: # no type safety to avoid a circular import
        factory_manager.add_factory(BaseFactory(
            name="Farm",
            description="Produces food.",
            input=[
                (Commodities.MONEY, 7)
            ],
            output=[
                (Commodities.FOOD, 7)
            ],
            cost=[
                (Commodities.MONEY, 455),
                (Commodities.BUILDING_MATERIALS, 250)
            ],
            category="food"
        ))
        factory_manager.add_factory(BaseFactory(
            name="Fishery",
            description="Fishes for fish and produces food.",
            input=[
                (Commodities.MONEY, 3),
                (Commodities.POWER, 6)
            ],
            output=[
                (Commodities.FOOD, 10)
            ],
            cost=[
                (Commodities.MONEY, 600),
                (Commodities.BUILDING_MATERIALS, 250)
            ],
            category="food"
        ))
        pass