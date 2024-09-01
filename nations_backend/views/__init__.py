from .user_views import signup_user, login_user, user_info, get_notifications, read_notification
from .nation_views import create_nation, nation_info, nation_factories, collect_taxes, nation_buildings, get_nation_by_id, upgrade, upgrades
from .factory_views import get_all_factories, build_factory, collect_from_factory
from .alliance_views import get_alliance_list, leave_alliance, create_alliance, post_alliance_shout, get_join_requests, join_alliance, accept_join_request, delete_alliance, get_alliance_by_id, get_alliance_list_pagination, get_alliance_members, kick_member, transfer_ownership, promote_member, demote_member
from .building_views import get_all_buildings, build_building

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest, JsonResponse
from ..models import Nation
from ..ticking import TickNation
from ..utils import build_error_response, build_success_response
from http import HTTPStatus
import json

with open("secrets.json") as file:
    data = json.load(file)
    secret_key = data.get("tick_secret")

@require_http_methods(["POST"])
def tick_nations(request: HttpRequest) -> JsonResponse:
    if not request.headers.get("secret") == secret_key:
        return build_error_response(
        "You don't have permission for this", HTTPStatus.UNAUTHORIZED
    )

    nations: list[Nation] = Nation.objects.all()
    [TickNation(nation).run_tick() for nation in nations]

    return build_success_response(
        "Ticked.", HTTPStatus.OK, safe=False
    )
