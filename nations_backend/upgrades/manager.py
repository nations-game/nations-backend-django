from .base import BaseUpgrade

class UpgradeManager:
    def __init__(self, upgrades: list[BaseUpgrade]) -> None:
        self.upgrades = upgrades

        self.create_initial_upgrades()
        pass

    def add_upgrade(self, upgrade: BaseUpgrade) -> None:
        self.buildings.append(upgrade)

    def get_building_by_id(self, id: str) -> BaseUpgrade:
        for upgrade in self.upgrades:
            if upgrade.id == id:
                return upgrade
        
        return None
    
    def get_buildings(self) -> list[BaseUpgrade]: return self.buildings
    
    def create_initial_upgrades(self) -> None:
        ...
