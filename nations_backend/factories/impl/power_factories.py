from ..base import BaseFactory, Commodities

class PowerFactories:
    def __init__(self, factory_manager) -> None: # no type safety to avoid a circular import
        factory_manager.add_factory(BaseFactory(
            name="Windmill",
            description="Produces power with the wind.",
            input=[
                (Commodities.MONEY, 6)
            ],
            output=[
                (Commodities.POWER, 6)
            ],
            cost=[
                (Commodities.MONEY, 365),
                (Commodities.BUILDING_MATERIALS, 152)
            ],
            category="power"
        ))
        factory_manager.add_factory(BaseFactory(
            name="Hydro Plant",
            description="Produces power with the water.",
            input=[
                (Commodities.MONEY, 9)
            ],
            output=[
                (Commodities.POWER, 16)
            ],
            cost=[
                (Commodities.MONEY, 504),
                (Commodities.BUILDING_MATERIALS, 302),
                (Commodities.METAL, 76),
            ],
            category="power"
        ))
        pass