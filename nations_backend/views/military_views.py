import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ..models import User, Nation, NationDivision
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
