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
                (Commodities.FOOD, 3)
            ],
            cost=[
                (Commodities.MONEY, 734),
                (Commodities.BUILDING_MATERIALS, 306)
            ]
        ))
        pass