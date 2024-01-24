from .base import BaseFactory, Commodities
from typing import List

class FactoryManager:
    def __init__(self) -> None:
        self.factories: List[BaseFactory] = []

        self.create_initial_factories()
        pass

    def add_factory(self, factory: BaseFactory) -> None:
        self.factories.append(factory)

    def get_factory_by_id(self, id: str) -> BaseFactory:
        for factory in self.factories:
            if factory.id == id:
                return factory
        
        return None
    
    def get_factories(self) -> List[BaseFactory]: return self.factories
    
    def create_initial_factories(self) -> None:
        self.add_factory(BaseFactory(
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

        self.add_factory(BaseFactory(
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

        self.add_factory(BaseFactory(
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

factory_manager = FactoryManager()