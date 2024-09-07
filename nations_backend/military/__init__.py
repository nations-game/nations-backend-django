from .unit_manager import UnitManager
from .unit_type import UnitType, UnitCategories
from ..util import Commodities

unit_manager: UnitManager = UnitManager()

unit_manager.add_unit(UnitType(
    name="National Guard",
    max_health=50,
    att=2,
    defense=1,
    recruit_cost=[
        (Commodities.MONEY, 480)
    ],
    upkeep=[
        (Commodities.FOOD, 1),
        (Commodities.MONEY, 1)
    ],
    category=UnitCategories.INFANTRY
))