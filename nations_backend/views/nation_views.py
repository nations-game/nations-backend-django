from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods

from ..decorators import parse_json, needs_auth, needs_nation
from ..factories import BaseFactory, factory_manager
from ..buildings import BaseBuilding, building_manager
from ..models import User, Nation, NationFactory, NationUpgrade
from ..utils import build_error_response, build_success_response
from ..util import Commodities
from ..upgrades import upgrade_manager

@needs_auth
@require_http_methods(["POST"])
@parse_json(
    ("name", str),
    ("system", int),
)
def create_nation(request: HttpRequest, name: str, system: int) -> JsonResponse:
    user: User = request.user

    if user.nation is not None:
        return build_error_response(
            "User already has a nation!", HTTPStatus.BAD_REQUEST
        )

    nation: Nation = Nation.objects.create(
        name=name,
        system=system,
        leader=user
    )
    
    user.nation = nation
    user.save()

    return build_success_response(
        nation.to_dict(), HTTPStatus.CREATED
    )

@needs_nation
@require_http_methods(["GET"])
def nation_info(request: HttpRequest) -> JsonResponse:
    user: User = request.user

    nation: Nation = user.nation
    return build_success_response(
        nation.to_dict(), HTTPStatus.OK
    )

@needs_nation
@require_http_methods(["GET"])
def nation_factories(request: HttpRequest) -> JsonResponse:
    user: User = request.user

    nation: Nation = user.nation

    factory_info_dict = {}

    for nation_factory in nation.get_factories():
        factory_type_id = nation_factory.factory_type
        factory_type_info = factory_manager.get_factory_by_id(factory_type_id).__dict__()
        ticks_run = nation_factory.ticks_run

        if factory_type_id not in factory_info_dict:
            factory_info_dict[factory_type_id] = {
                "info": factory_type_info,
                "ticks_run": ticks_run,
                "quantity": 1 
            }
        else:
            factory_info_dict[factory_type_id]["ticks_run"] += ticks_run
            factory_info_dict[factory_type_id]["quantity"] += 1

    factory_info_list = list(factory_info_dict.values())

    # Set safe to false in order to send list 
    return build_success_response(
        factory_info_list, HTTPStatus.OK, safe=False 
    )

@needs_nation
@require_http_methods(["GET"])
def nation_buildings(request: HttpRequest) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    building_info_list = []

    for nation_building in nation.get_buildings():
        building_type_id = nation_building.building_type
        building_type_info = building_manager.get_building_by_id(building_type_id).__dict__()
        level = nation_building.level

        info_dict = building_type_info
        info_dict.update({ "level": level })
        building_info_list.append(info_dict)

    # Set safe to false in order to send list 
    return build_success_response(
        building_info_list, HTTPStatus.OK, safe=False 
    )


@needs_nation
@require_http_methods(["POST"])
def collect_taxes(request: HttpRequest) -> JsonResponse:
    user: User = request.user

    nation: Nation = user.nation
    taxes = nation.taxes_to_collect
    nation.money += taxes
    nation.taxes_to_collect = 0
    nation.save()

    return build_success_response(
        nation.to_dict(), HTTPStatus.OK
    )

@require_http_methods(["POST"])
@parse_json(
    ("id", int),
)
def get_nation_by_id(request: HttpRequest, id: int) -> JsonResponse:
    nation: Nation = Nation.objects.get(id=id)

    nation_dict = nation.to_dict()

    leader_dict = nation.leader.to_dict()
    del leader_dict["email"]

    nation_dict.update({
        "leader": leader_dict
    })

    return build_success_response(
        nation_dict, HTTPStatus.OK
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json(
    ("upgrade_id", str)
)
def upgrade(request: HttpRequest, upgrade_id: str) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    nation_upgrade = NationUpgrade.objects.filter(nation=nation, upgrade_type=upgrade_id).first()

    if nation_upgrade is None:
        nation_upgrade = NationUpgrade.objects.create(
            nation=nation,
            upgrade_type=upgrade_id,
            level=0
        )

    upgrade = upgrade_manager.get_upgrade_by_id(upgrade_id)

    commodity: Commodities
    quantity: int
    can_afford = True
    for commodity, quantity in upgrade.get_cost(max(1, nation_upgrade.level)):
        match commodity.value:
            case "money": 
                if quantity > nation.money: can_afford = False
            case "food": 
                if quantity > nation.food: can_afford = False
            case "power": 
                if quantity > nation.power: can_afford = False
            case "building_materials": 
                if quantity > nation.building_materials: can_afford = False
            case "metal": 
                if quantity > nation.metal: can_afford = False
            case "consumer_goods": 
                if quantity > nation.consumer_goods: can_afford = False

    if not can_afford:
        return build_error_response(
            "You can't afford that!", HTTPStatus.BAD_REQUEST
        )

    for commodity, quantity in upgrade.get_cost(max(1, nation_upgrade.level)):
        match commodity.value:
            case "money": 
                if quantity < nation.money: nation.money -= quantity
            case "food": 
                if quantity < nation.food: nation.food -= quantity
            case "power": 
                if quantity < nation.power: nation.power -= quantity
            case "building_materials": 
                if quantity < nation.building_materials: nation.building_materials -= quantity
            case "metal": 
                if quantity < nation.metal: nation.metal -= quantity
            case "consumer_goods": 
                if quantity < nation.consumer_goods: nation.consumer_goods -= quantity
    
    nation.save()
    nation_upgrade.level += 1
    nation_upgrade.save()

    return build_success_response(
        "Upgraded!", HTTPStatus.CREATED
    )