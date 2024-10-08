from .manager import BuildingManager
from .base import BaseBuilding
from ..util import Commodities

_building_list = []

_building_list.append(
    BaseBuilding(
        name="Research Lab",
        description="Research different technologies.",
        max_level=5,
        cost=[
            (Commodities.UNUSED_LAND, 1)
        ]
    )
)

_building_list.append(
    BaseBuilding(
        name="Barracks",
        description="Recruit different military units.",
        max_level=5,
        cost=[
            (Commodities.MONEY, 500),
            (Commodities.BUILDING_MATERIALS, 250),
            (Commodities.UNUSED_LAND, 5)
        ]
    )
)

building_manager = BuildingManager(buildings=_building_list)