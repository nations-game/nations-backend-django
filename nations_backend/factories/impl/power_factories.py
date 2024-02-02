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
            ]
        ))
        pass