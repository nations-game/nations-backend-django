import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import User, Nation, Alliance, AllianceMember, AllianceRequest
from ..decorators import parse_json, needs_nation
from ..utils import build_error_response, build_success_response

@needs_nation
@require_http_methods(["GET"])
def get_alliance_list(request: HttpRequest) -> JsonResponse:
    alliance_list = []
    alliance_objs = Alliance.objects.all()

    for alliance_obj in alliance_objs:
        alliance_list.append({
            "name": alliance_obj.name,
            "icon": alliance_obj.icon,
            "status": "public" if alliance_obj.public else "private",
            "member_count": alliance_obj.get_member_count(),
            "owner_nation": alliance_obj.get_alliance_owner().nation
        })

    return build_success_response(
        alliance_list, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["GET"])
@parse_json([
    ("name", str),
    ("icon", str),
    ("public", bool),
])
def create_alliance(request: HttpRequest, name: str, icon: str, public: bool) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

