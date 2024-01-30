import json, time
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
            "id": alliance_obj.id,
            "name": alliance_obj.name,
            "icon": alliance_obj.icon,
            "status": "public" if alliance_obj.public else "private",
            "member_count": alliance_obj.get_member_count(),
            "owner_nation_id": alliance_obj.get_alliance_owner().nation.id
        })

    return build_success_response(
        alliance_list, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("name", str),
    ("icon", str),
    ("public", bool),
])
def create_alliance(request: HttpRequest, name: str, icon: str, public: bool) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    if nation.get_alliance() is not None:
        return build_error_response(
            "You are already the member of an alliance!", 401
        )

    alliance = Alliance.objects.create(
        name=name,
        icon=icon,
        public=public
    )

    alliance_member = AllianceMember.objects.create(
        alliance=alliance,
        nation=nation,
        role=2 # Owner role
    )

    return build_success_response(
        f"Successfully created alliance {alliance.name} with id {alliance.id}", 201
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("id", int)
])
def join_alliance(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    if nation.get_alliance() is not None:
        return build_error_response(
            "You are already the member of an alliance!", 401
        )

    alliance = Alliance.objects.filter(id=id).first()

    if alliance.public:
        alliance_member = AllianceMember.objects.create(
            alliance=alliance,
            nation=nation,
            role=0 # Member role
        )

        return build_success_response(
            f"Successfully joined {alliance.name}!", 201
        )
    else:
        join_request = AllianceRequest.objects.create(
            timestamp=int(time.time()),
            requesting_nation=nation,
            alliance=alliance
        )

        return build_success_response(
            f"Sent join request to {alliance.name}!", 200
        )

@needs_nation
@require_http_methods(["POST"])
def get_join_requests(request: HttpRequest) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role == 0:
        return build_error_response(
            "You are unauthorized to do this!", 401
        )

    alliance = alliance_member.alliance

    join_requests = AllianceRequest.objects.filter(alliance=alliance).all()
    requesting_nations = []

    for req in join_requests:
        requesting_nations.append({
            "id": req.id,
            "nation": req.nation.to_dict()
        })

    return build_success_response(
        requesting_nations, 200, safe=False
    )