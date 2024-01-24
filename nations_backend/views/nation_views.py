from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import User, Nation, NationFactory, FactoryType

import json

@require_http_methods(["POST"])
def create_nation(request: HttpRequest) -> JsonResponse:
    if request.user is None:
        return JsonResponse({
            "status": "error",
            "details": "Not authenticated!"
        }, status=401)
    
    user: User = request.user

    if user.nation is not None:
        return JsonResponse({
            "status": "error",
            "details": "User already has a nation!"
        }, status=400)
    
    if not request.body:
        return JsonResponse({
            "status": "error",
            "details": "Malformed request."
        }, status=400)

    request_data: dict = json.loads(request.body)
    
    name: str = request_data.get("name")
    system: str = request_data.get("system")

    nation: Nation = Nation.objects.create(
        name=name,
        system=system,
        leader=user
    )

    # Auto add factories for debugging
    NationFactory.objects.create(
        nation=nation,
        factory_type=FactoryType.objects.filter(name="Farm").first()
    )

    NationFactory.objects.create(
        nation=nation,
        factory_type=FactoryType.objects.filter(name="Clothes Factory").first()
    )

    NationFactory.objects.create(
        nation=nation,
        factory_type=FactoryType.objects.filter(name="Hydro Power Plant").first()
    )
    user.nation = nation
    user.save()

    return JsonResponse({
        "status": "success",
        "details": nation.to_dict()
    }, status=200)

@require_http_methods(["GET"])
def nation_info(request: HttpRequest) -> JsonResponse:
    if request.user is None:
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

    nation: Nation = user.nation
    return JsonResponse(nation.to_dict())

@require_http_methods(["GET"])
def nation_factories(request: HttpRequest) -> JsonResponse:
    return HttpResponse("hi mom!!")

@require_http_methods(["POST"])
def build_factory(request: HttpRequest) -> JsonResponse:
    request_data: dict = json.loads(request.body)
    if request.user is None:
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
    
    nation: Nation = user.nation

    type = request_data.get("type")
    factory_type = FactoryType.objects.filter(name=type).first()

    if factory_type is None:
        return JsonResponse({
            "status": "error",
            "details": "Invalid factory"
        }, 400)
    
    # The following code will most likely not work
    # I don't quite understand how this works???
    NationFactory.objects.filter(nation).create(factory_type)

    return JsonResponse({"status": "success"})

@require_http_methods(["POST"])
def collect_from_factory(request: HttpRequest) -> JsonResponse:
    request_data: dict = json.loads(request.body)
    if request.user is None:
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
    
    nation: Nation = user.nation

    factory_id = request_data.get("factory_id")
    if factory_id is None:
        return JsonResponse({
            "status": "error",
            "details": "Invalid factory!"
        }, status=401)

    factory: NationFactory = NationFactory.objects.filter(nation=nation, id=factory_id).first()

    if factory is None:
        return JsonResponse({
            "status": "error", 
            "details": "Invalid factory ID"
        }), 400

    if factory.production_resources > 0:
        match factory.factory_type.commodity:
            case "food":
                nation.food += factory.factory_type.production * factory.factory_type.current_level
            case "consumer_goods":
                nation.consumer_goods += factory.factory_type.production * factory.factory_type.current_level
            case "power":
                nation.power += factory.factory_type.production * factory.factory_type.current_level
        return JsonResponse({
            "status": "success"
        }, 200)
    else:
        return JsonResponse({"status": "error", "details": "Not enough resources to collect"})