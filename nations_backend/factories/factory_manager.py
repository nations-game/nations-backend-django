from .base import BaseFactory, Commodities
from typing import List
from .impl import ConsumerGoodsFactories, FoodFactories, PowerFactories

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
        FoodFactories(self)
        PowerFactories(self)
        ConsumerGoodsFactories(self)
