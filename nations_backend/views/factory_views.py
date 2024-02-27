import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

from ..models import User, Nation, NationFactory
from ..factories import factory_manager, BaseFactory, Commodities
from ..decorators import parse_json, needs_nation
from ..utils import build_error_response, build_success_response

@needs_nation
@require_http_methods(["GET"])
@cache_page(None) # I'm assuming this is static - Please remove the forever cache if otherwise
def get_all_factories(request: HttpRequest) -> JsonResponse:
    factory_info_list = [factory.__dict__() for factory in factory_manager.get_factories()]

    # Set safe to false in order to send list 
    return build_success_response(
        factory_info_list, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("factory_id", str)
])
def build_factory(request: HttpRequest, factory_id: str) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation
    
    factory: BaseFactory = factory_manager.get_factory_by_id(factory_id)
    
    if factory is None:
        return build_error_response(
            "Factory not found!", HTTPStatus.BAD_REQUEST
        )

    commodity: Commodities
    quantity: int
    can_afford = True
    for commodity, quantity in factory.cost:
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
    
    for commodity, quantity in factory.cost:
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
    
    nation_factory: NationFactory = NationFactory.objects.create(
        nation=nation,
        factory_type=factory_id
    )

    return build_success_response(
        "Built Factory!", HTTPStatus.CREATED
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("factory_id", str)
])
def collect_from_factory(request: HttpRequest, factory_id: str) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    base_factory: BaseFactory = factory_manager.get_factory_by_id(factory_id)

    nation_factories = NationFactory.objects.filter(factory_type=factory_id).all()

    if not nation_factories:
        return build_error_response(
            "Invalid Factory ID", HTTPStatus.BAD_REQUEST
        )
    
    # It should have already taken away this when doing the production stuff
    for nation_factory in nation_factories:
        for _ in range(nation_factory.ticks_run):
            for commodity, quantity in base_factory.output:
                match commodity.value:
                    case "money": 
                        if quantity < nation.money: nation.money += quantity
                    case "food": 
                        if quantity < nation.food: nation.food += quantity
                    case "power": 
                        if quantity < nation.power: nation.power += quantity
                    case "building_materials": 
                        if quantity < nation.building_materials: nation.building_materials += quantity
                    case "metal": 
                        if quantity < nation.metal: nation.metal += quantity
                    case "consumer_goods": 
                        if quantity < nation.consumer_goods: nation.consumer_goods += quantity
        nation_factory.ticks_run = 0 # removed for debugging
        nation_factory.save()
    
    nation.save()
    

    return build_success_response(
        "Collected From Factory", HTTPStatus.OK
    )