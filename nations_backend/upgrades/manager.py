from .base import BaseUpgrade
from ..models.nation import Nation, NationUpgrade

import random

class UpgradeManager:
    def __init__(self, upgrades: list[BaseUpgrade]) -> None:
        self.upgrades = upgrades

        self.create_initial_upgrades()
        pass

    def add_upgrade(self, upgrade: BaseUpgrade) -> None:
        self.upgrades.append(upgrade)

    def perform_upgrade(self, nation: Nation, nation_upgrade: NationUpgrade, upgrade_id: str) -> None:
        match upgrade_id:
            case "expand_borders":
                current_size = nation.land

                added_land = current_size * (random.randint(1, 5) * 0.01)

                nation.land += added_land
                nation.unused_land += added_land
                nation.save()
                pass

    def get_upgrade_by_id(self, id: str) -> BaseUpgrade:
        for upgrade in self.upgrades:
            if upgrade.id == id:
                return upgrade
        
        return None
    
    def get_upgrades(self) -> list[BaseUpgrade]: return self.upgrades
    
    def create_initial_upgrades(self) -> None:
        ...
