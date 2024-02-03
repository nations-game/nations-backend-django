from .base import BaseBuilding


class BuildingManager:
    def __init__(self, buildings: list[BaseBuilding]) -> None:
        self.buildings = buildings

    