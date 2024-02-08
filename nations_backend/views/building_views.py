import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import User, Nation, NationBuilding
from ..factories import Commodities
from ..buildings import building_manager, BaseBuilding
from ..decorators import parse_json, needs_nation
from ..utils import build_error_response, build_success_response

@needs_nation
@require_http_methods(["GET"])
def get_all_buildings(request: HttpRequest) -> JsonResponse:
    building_info_list = []

    for building in building_manager.get_buildings():
        building_info_list.append(building.__dict__())

    # Set safe to false in order to send list 
    return build_success_response(
        building_info_list, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["GET"])
@parse_json([
    ("building_id", str)
])
def build_building(request: HttpRequest, building_id: str) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation
    building = building_manager.get_building_by_id(building_id)

    existing_building = NationBuilding.objects.filter(nation=nation, building_type=building_id).first()
    if existing_building is not None:
        return build_error_response(
            "You already have that building!", HTTPStatus.BAD_REQUEST
        )

    commodity: Commodities
    quantity: int
    can_afford = True
    for commodity, quantity in building.cost:
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
    
    for commodity, quantity in building.cost:
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

    nation_building = NationBuilding.objects.create(
        nation=nation,
        building_type=building_id
    )

    return build_success_response(
        "Built building!", HTTPStatus.CREATED
    )