from ..base import BaseFactory, Commodities

class BuildingMaterialsFactories:
    def __init__(self, factory_manager) -> None: # no type safety to avoid a circular import
        factory_manager.add_factory(BaseFactory(
            name="Quarry",
            description="Produces building materials.",
            input=[
                (Commodities.MONEY, 4),
                (Commodities.POWER, 7)
            ],
            output=[
                (Commodities.BUILDING_MATERIALS, 8)
            ],
            cost=[
                (Commodities.MONEY, 952)
            ],
            category="bm"
        ))
        factory_manager.add_factory(BaseFactory(
            name="Sawmill",
            description="Produces building materials.",
            input=[
                (Commodities.MONEY, 4),
                (Commodities.POWER, 7)
            ],
            output=[
                (Commodities.BUILDING_MATERIALS, 8)
            ],
            cost=[
                (Commodities.MONEY, 952)
            ],
            category="bm"
        ))
        pass