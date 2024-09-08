import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ..models import User, Nation, NationDivision, DivisionUnit
from ..military import unit_manager, UnitType, UnitCategories
from ..decorators import parse_json, needs_nation
from ..utils import build_error_response, build_success_response
from ..util import Commodities

@needs_nation
@require_http_methods(["GET"])
@cache_page(None) # I'm assuming this is static - Please remove the forever cache if otherwise
def get_all_units(request: HttpRequest) -> JsonResponse:
    unit_info_list = [unit.__dict__() for unit in unit_manager.get_units()]

    # Set safe to false in order to send list 
    return build_success_response(
        unit_info_list, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["GET"])
def nation_divisions(request: HttpRequest) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation
    divisions = []

    for division in nation.get_divisions():
        divisions.append(division.to_dict())

    # Set safe to false in order to send list 
    return build_success_response(
        divisions, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json(
    ("name", str)
)
def add_division(request: HttpRequest, name: str) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    duplicate_div = NationDivision.objects.filter(nation=nation, name=name).first()

    if duplicate_div:
        return build_error_response(
            "A division with this name already exists!", HTTPStatus.BAD_REQUEST
        )
    
    NationDivision.objects.create(
        nation=nation,
        name=name
    )

    return build_success_response(
        f"Division {name} has sucessfully been created!", HTTPStatus.CREATED
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json(
    ("unit_id", str)
)
def recruit_unit(request: HttpRequest, unit_id: str) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation
    
    unit: UnitType = unit_manager.get_unit_by_id(unit_id)

    if unit is None:
        return build_error_response(
            "This unit type does not exist!", HTTPStatus.NOT_FOUND
        )

    commodity: Commodities
    quantity: int
    can_afford = True
    for commodity, quantity in unit.recruit_cost:
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
            case "unused_land": 
                if quantity > nation.unused_land: can_afford = False
                
    if not can_afford:
        return build_error_response(
            "You can't afford that!", HTTPStatus.BAD_REQUEST
        )
    
    for commodity, quantity in unit.recruit_cost:
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
            case "unused_land": 
                if quantity < nation.unused_land: nation.unused_land -= quantity
    
    nation.save()
    
    military_unit: DivisionUnit = DivisionUnit.objects.create(
        division=nation.get_reserve_division(),
        unit_type=unit_id,
        health=unit.max_health
    )

    return build_success_response(
        "Succesfully recruited unit!", HTTPStatus.CREATED
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json(
    ("unit_id", int),
    ("old_div", str),
    ("new_div", str)
)
def move_unit(request: HttpRequest, unit_id: int, old_div: str, new_div: str) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    unit: DivisionUnit = DivisionUnit.objects.filter(id=unit_id).first()

    if unit is None:
        return build_error_response(
            "Unit does not exist!", HTTPStatus.NOT_FOUND
        )
    
    old_division = NationDivision.objects.filter(name=old_div, nation=nation).first()

    if old_division is None:
        return build_error_response(
            "Division to move from does not exist!", HTTPStatus.NOT_FOUND
        )
    
    new_division = NationDivision.objects.filter(name=new_div, nation=nation).first()

    if new_division is None:
        return build_error_response(
            "Division to move to does not exist!", HTTPStatus.NOT_FOUND
        )
    
    unit.division = new_division

    unit.save()

    return build_success_response(
        "Successfully moved unit!", HTTPStatus.OK
    )
