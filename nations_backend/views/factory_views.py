from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import User, Nation, NationFactory
from ..factories import factory_manager, BaseFactory, Commodities

import json

@require_http_methods(["GET"])
def get_all_factories(request: HttpRequest) -> JsonResponse:
    if request.user is None or request.user.is_anonymous:
        return JsonResponse({
            "status": "error",
            "details": "Not authenticated!"
        }, status=401)
    
    user: User = request.user

    if user.nation is None:
        return JsonResponse({
            "status": "error",
            "details": "User does not have a nation!"
        }, status=401)
    
    factory_info_list = []

    for factory in factory_manager.get_factories():
        factory_info_list.append(factory.__dict__())

    return JsonResponse(factory_info_list, safe=False)

@require_http_methods(["POST"])
def build_factory(request: HttpRequest) -> JsonResponse:
    if request.user is None or request.user.is_anonymous:
        return JsonResponse({
            "status": "error",
            "details": "Not authenticated!"
        }, status=401)
    
    if not request.body:
        return JsonResponse({
            "status": "error",
            "details": "Malformed request."
        }, status=400)
    
    user: User = request.user

    if user.nation is None:
        return JsonResponse({
            "status": "error",
            "details": "User does not have a nation!"
        }, status=401)
    
    nation: Nation = user.nation
    
    request_data: dict = json.loads(request.body)
    
    factory_id: str = request_data.get("factory_id")
    factory: BaseFactory = factory_manager.get_factory_by_id(factory_id)

    if factory is None:
        return JsonResponse({
            "status": "error",
            "details": "Factory not found!"
        }, status=400)

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
        return JsonResponse({
            "status": "error",
            "details": "You can't afford that!"
        }, status=400)
    
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

    return JsonResponse({
        "status": "success",
        "details": "Built factory!"
    }, status=200)

@require_http_methods(["POST"])
def collect_from_factory(request: HttpRequest) -> JsonResponse:
    if request.user is None or request.user.is_anonymous:
        return JsonResponse({
            "status": "error",
            "details": "Not authenticated!"
        }, status=401)
    
    if not request.body:
        return JsonResponse({
            "status": "error",
            "details": "Malformed request."
        }, status=400)
    
    user: User = request.user

    if user.nation is None:
        return JsonResponse({
            "status": "error",
            "details": "User does not have a nation!"
        }, status=401)
    
    nation: Nation = user.nation

    request_data: dict = json.loads(request.body)
    factory_id: str = request_data.get("factory_id")
    base_factory: BaseFactory = factory_manager.get_factory_by_id(factory_id)

    nation_factories = NationFactory.objects.filter(factory_type=factory_id).all()

    if nation_factories is None or len(nation_factories) == 0:
        return JsonResponse({
            "status": "error",
            "details": "Invalid factory ID."
        }, status=400)
    
    # It should have already taken away this when doing the production stuff
    for nation_factory in nation_factories:
        for _ in range(nation_factory.ticks_run):
            for commodity, quantity in base_factory.output:
                print(commodity.value, quantity)
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
    
    nation.save()
    nation_factory.ticks_run = 0 # removed for debugging
    nation_factory.save()

    return JsonResponse({
        "status": "success",
        "details": "Collected from factory!"
    }, status=200)