from ..base import BaseFactory, Commodities

class ConsumerGoodsFactories:
    def __init__(self, factory_manager) -> None: # no type safety to avoid a circular import
        factory_manager.add_factory(BaseFactory(
            name="Clothes Factory",
            description="Makes clothes for your citizens.",
            input=[
                (Commodities.MONEY, 3),
                (Commodities.POWER, 5)
            ],
            output=[
                (Commodities.CONSUMER_GOODS, 2)
            ],
            cost=[
                (Commodities.MONEY, 396),
                (Commodities.BUILDING_MATERIALS, 238)
            ]
        ))
        pass