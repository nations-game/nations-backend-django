from .unit_type import UnitType, UnitCategories
from typing import List

class UnitManager:
    def __init__(self) -> None:
        self.units: List[UnitType] = []
        pass

    def add_unit(self, unit: UnitType) -> None:
        self.units.append(unit)
    
    def get_unit_by_id(self, id: str) -> UnitType:
        for unit in self.units:
            if unit.id == id:
                return unit
        
        return None
    
    def get_units_in_category(self, category: UnitCategories) -> List[UnitType]:
        cat_units = []
        for unit in self.units:
            if unit.category == category:
                cat_units.add(unit)
        return cat_units
    
    def get_units(self) -> List[UnitType]: return self.units