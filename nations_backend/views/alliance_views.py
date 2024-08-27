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
@require_http_methods(["GET", "POST"])
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
@require_http_methods(["GET"])
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
            "nation": req.requesting_nation.to_dict()
        })

    return build_success_response(
        requesting_nations, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("id", int)
])
def accept_join_request(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role == AllianceRole.MEMBER:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )

    alliance = alliance_member.alliance
    alliance_request = AllianceRequest.objects.filter(id=id).first()

    if alliance_request is not None:
        alliance_member = AllianceMember.objects.create(
            alliance=alliance,
            nation=alliance_request.requesting_nation,
            role=AllianceRole.MEMBER
        )

        alliance_request.delete()

        return build_success_response(
            f"Successfully joined {alliance.name}!", HTTPStatus.OK
        )


@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("id", int)
])
def get_alliance_members(request: HttpRequest, id: int) -> JsonResponse:
    alliance = Alliance.objects.filter(id=id).first()

    if alliance is None:
        return build_error_response(
            f"Alliance with id {id} not found!", HTTPStatus.NOT_FOUND
        )
    
    members = AllianceMember.objects.filter(alliance=alliance).all()
    member_nations = []

    for req in members:
        nation = req.nation.to_dict()
        nation.update({
            "alliance_role": "member" if req.role == 0 else "admin" if req.role == 1 else "owner" if req.role == 2 else "error"
        })
        member_nations.append(nation)

    return build_success_response(
        member_nations, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["POST"])
def leave_alliance(request: HttpRequest) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    if nation.get_alliance() is None:
        return build_error_response(
            "You are not a member of an alliance!", HTTPStatus.BAD_REQUEST
        )

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None:
        return build_error_response(
            "You are not a member of an alliance!", HTTPStatus.BAD_REQUEST
        )

    if alliance_member.role is AllianceRole.OWNER:
        return build_error_response(
            "You are the owner of this alliance, you must transfer ownership or delete it!", HTTPStatus.BAD_REQUEST
        )
    
    alliance_member.delete()

    return build_success_response(
        "Left alliance!", HTTPStatus.OK
    )

@needs_nation
@require_http_methods(["POST"])
def delete_alliance(request: HttpRequest) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role != 2:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )

    alliance = alliance_member.alliance
    alliance_name = alliance.name
    alliance.delete()
    return build_success_response(
        f"Successfully deleted {alliance_name}!", HTTPStatus.OK
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("id", int)
])
def kick_member(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role < AllianceRole.ADMIN:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    kicked_nation = Nation.objects.filter(id=id).first()

    if kicked_nation == nation:
        return build_error_response(
            "You can't kick yourself!", HTTPStatus.BAD_REQUEST
        )

    if kicked_nation is None:
        return build_error_response(
            "The nation you are trying to kick doesn't exist!", HTTPStatus.BAD_REQUEST
        )

    kicked_member = AllianceMember.objects.filter(nation=kicked_nation).first()

    if kicked_member is None:
        return build_error_response(
            "The nation you are trying to kick isn't in this alliance!", HTTPStatus.BAD_REQUEST
        )
    
    kicked_member.delete()

    return build_success_response(
        f"Successfully kicked {kicked_nation.name}!", HTTPStatus.OK
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("id", int)
])
def promote_member(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role < AllianceRole.OWNER:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    promoted_nation = Nation.objects.filter(id=id).first()

    if promoted_nation == nation:
        return build_error_response(
            "You can't promote yourself!", HTTPStatus.BAD_REQUEST
        )

    if promoted_nation is None:
        return build_error_response(
            "The nation you are trying to promote doesn't exist!", HTTPStatus.BAD_REQUEST
        )

    promoted_member = AllianceMember.objects.filter(nation=promoted_nation).first()

    if promoted_member is None:
        return build_error_response(
            "The nation you are trying to promote isn't in this alliance!", HTTPStatus.BAD_REQUEST
        )
    
    promoted_member.role = AllianceRole.ADMIN
    promoted_member.save()

    return build_success_response(
        f"Successfully promoted {promoted_nation.name}!", HTTPStatus.OK
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("id", int)
])
def demote_member(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role < AllianceRole.OWNER:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    demoted_nation = Nation.objects.filter(id=id).first()

    if demoted_nation == nation:
        return build_error_response(
            "You can't demote yourself!", HTTPStatus.BAD_REQUEST
        )

    if demoted_nation is None:
        return build_error_response(
            "The nation you are trying to demote doesn't exist!", HTTPStatus.BAD_REQUEST
        )

    demoted_member = AllianceMember.objects.filter(nation=demoted_nation).first()

    if demoted_member is None:
        return build_error_response(
            "The nation you are trying to demote isn't in this alliance!", HTTPStatus.BAD_REQUEST
        )
    
    demoted_member.role = AllianceRole.MEMBER
    demoted_member.save()

    return build_success_response(
        f"Successfully demoted {demoted_nation.name}!", HTTPStatus.OK
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json([
    ("id", int)
])
def transfer_ownership(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role != AllianceRole.OWNER:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    transferred_nation = Nation.objects.filter(id=id).first()

    if transferred_nation is None:
        return build_error_response(
            "The nation you are trying to transfer to doesn't exist!", HTTPStatus.BAD_REQUEST
        )

    transferred_member = AllianceMember.objects.filter(nation=transferred_nation).first()

    if transferred_member is None:
        return build_error_response(
            "The nation you are trying to transfer to isn't in this alliance!", HTTPStatus.BAD_REQUEST
        )
    
    alliance_member.role = AllianceRole.ADMIN
    alliance_member.save()
    
    transferred_member.role = AllianceRole.OWNER
    transferred_member.save()

    return build_success_response(
        f"Transferred ownership of {transferred_member.alliance.name} to {transferred_nation.name}!", HTTPStatus.OK
    )
