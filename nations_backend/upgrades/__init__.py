from .manager import UpgradeManager
from .base import BaseUpgrade
from ..util import Commodities

_upgrade_list = []

_upgrade_list.append(
    BaseUpgrade(
        name="Expand Borders",
        description="Expand your nation's borders!",
        base_cost=[
            (Commodities.MONEY, 10_000),
            (Commodities.FOOD, 1000),
            (Commodities.BUILDING_MATERIALS, 1000),
            (Commodities.POWER, 1000)
        ]
    )
)
upgrade_manager = UpgradeManager(upgrades=_upgrade_list)