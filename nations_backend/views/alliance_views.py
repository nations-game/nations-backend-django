import json, time
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

from ..models import User, Nation, Alliance, AllianceMember, AllianceRequest, AllianceShout, AllianceRole
from ..decorators import parse_json, needs_nation
from ..utils import build_error_response, build_success_response

@needs_nation
@require_http_methods(["GET"])
def get_alliance_list(request: HttpRequest) -> JsonResponse:
    alliance_list = [alliance.to_dict() for alliance in Alliance.objects.all()]

    return build_success_response(
        alliance_list, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("page", int),
    ("amount", int)
])
def get_alliance_list_pagination(request: HttpRequest, page: int, amount: int) -> JsonResponse:
    offset = page * amount
    alliance_page_list = sorted(Alliance.objects.all(), key=lambda x: x.get_member_count())
    alliance_page_list = alliance_page_list[offset:offset+amount]
    alliance_list = [alliance.to_dict() for alliance in alliance_page_list]

    return build_success_response(
        alliance_list, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["GET"])
@parse_json([
    ("id", int)
])
def get_alliance_by_id(request: HttpRequest, id: int) -> JsonResponse:
    alliance = Alliance.objects.filter(id=id).first()

    if alliance is None:
        return build_error_response(
            f"Alliance with id {id} not found!", HTTPStatus.NOT_FOUND
        )
    else:
        return build_success_response(
            alliance.to_dict(), HTTPStatus.OK
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
            "You are already the member of an alliance!", HTTPStatus.BAD_REQUEST
        )

    alliance = Alliance.objects.create(
        name=name,
        icon=icon,
        public=public
    )

    alliance_member = AllianceMember.objects.create(
        alliance=alliance,
        nation=nation,
        role=AllianceRole.OWNER
    )

    return build_success_response(
        f"Successfully created alliance {alliance.name} with id {alliance.id}", HTTPStatus.CREATED
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
            "You are already the member of an alliance!", HTTPStatus.BAD_REQUEST
        )

    alliance = Alliance.objects.filter(id=id).first()

    if alliance is None:
        return build_error_response(
            f"Alliance with id {id} not found!", HTTPStatus.NOT_FOUND
        )

    if alliance.public:
        alliance_member = AllianceMember.objects.create(
            alliance=alliance,
            nation=nation,
            role=AllianceRole.MEMBER
        )

        return build_success_response(
            f"Successfully joined {alliance.name}!", HTTPStatus.OK
        )
    else:
        join_request = AllianceRequest.objects.create(
            timestamp=int(time.time()),
            requesting_nation=nation,
            alliance=alliance
        )

        return build_success_response(
            f"Sent join request to {alliance.name}!", HTTPStatus.OK
        )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("shout_text", str)
])
def post_alliance_shout(request: HttpRequest, shout_text: str) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role == AllianceRole.MEMBER:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )

    alliance = alliance_member.alliance

    shout = AllianceShout.objects.create(
        shouting_nation=nation,
        text=shout_text
    )

    alliance.shout = shout
    alliance.save()

    return build_success_response(
        "Posted alliance shout!", HTTPStatus.CREATED, safe=False
    )

@needs_nation
@require_http_methods(["POST"])
def get_join_requests(request: HttpRequest) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role == AllianceRole.MEMBER:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
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
        requesting_nations, HTTPStatus.OK, safe=False
    )