from .base import BaseBuilding

class BuildingManager:
    def __init__(self, buildings: list[BaseBuilding]) -> None:
        self.buildings = buildings

        self.create_initial_buildings()
        pass

    def add_building(self, building: BaseBuilding) -> None:
        self.buildings.append(building)

    def get_building_by_id(self, id: str) -> BaseBuilding:
        for building in self.buildings:
            if building.id == id:
                return building
        
        return None
    
    def get_buildings(self) -> list[BaseBuilding]: return self.buildings
    
    def create_initial_buildings(self) -> None:
        ...
