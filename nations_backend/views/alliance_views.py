import json, time
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.db.models import Count, Q

from ..models import User, Nation, Alliance, AllianceMember, AllianceRequest, AllianceShout, AllianceRole, AllianceAllyRequest, AllianceAlly, AllianceEnemy
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
@parse_json(
    ("page", int),
    ("amount", int)
)
def get_alliance_list_pagination(request: HttpRequest, page: int, amount: int) -> JsonResponse:
    offset = page * amount
    
    alliance_page_list = Alliance.objects.annotate(member_count=Count('alliancemember')).order_by('-member_count')[offset:offset+amount]
    alliance_list = [alliance.to_dict() for alliance in alliance_page_list]

    return build_success_response(
        alliance_list, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["GET", "POST"])
@parse_json(
    ("id", int)
)
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
@parse_json(
    ("name", str),
    ("icon", str),
    ("public", bool),
)
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
        public=public,
        owner=nation
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
@parse_json(
    ("id", int)
)
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
@parse_json(
    ("shout_text", str)
)
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
@parse_json(
    ("id", int)
)
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
@parse_json(
    ("id", int)
)
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
@parse_json(
    ("id", int)
)
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

    if kicked_member.role > AllianceRole.MEMBER:
        return build_error_response(
            "You cannot kick this nation!", HTTPStatus.BAD_REQUEST
        )

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
@parse_json(
    ("id", int)
)
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
@parse_json(
    ("id", int)
)
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
@parse_json(
    ("id", int)
)
def transfer_ownership(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role != AllianceRole.OWNER:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    alliance: Alliance = alliance_member.alliance
    
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
    alliance.owner = transferred_member.nation
    alliance.save()
    transferred_member.save()

    return build_success_response(
        f"Transferred ownership of {transferred_member.alliance.name} to {transferred_nation.name}!", HTTPStatus.OK
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json(
    ("id", int)
)
def send_ally_request(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role < AllianceRole.ADMIN:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    receiving_alliance = Alliance.objects.filter(pk=id).first()

    if receiving_alliance is None:
        return build_error_response(
            "The alliance you are trying to request doesn't exist!", HTTPStatus.BAD_REQUEST
        )
    
    alliance = alliance_member.alliance

    if receiving_alliance == alliance:
        return build_error_response(
            "You cannot send a request to yourself!", HTTPStatus.BAD_REQUEST
        )
    
    exisiting_request = AllianceAllyRequest.objects.filter(requesting_alliance=alliance, alliance=receiving_alliance).first()

    if exisiting_request is not None:
        return build_error_response(
            "You already sent a request!", HTTPStatus.BAD_REQUEST
        )
    
    alliance_request = AllianceAllyRequest.objects.create(
        timestamp=time.time(),
        requesting_alliance=alliance,
        alliance=receiving_alliance
    )

    return build_success_response(
        "Successfully sent ally request!", HTTPStatus.CREATED
    )

@needs_nation
@require_http_methods(["GET"])
@parse_json(
    ("page", int),
    ("amount", int)
)
def get_ally_requests(request: HttpRequest, page: int, amount: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    offset = page * amount

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role < AllianceRole.ADMIN:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    ally_requests = AllianceAllyRequest.objects.filter(alliance=alliance_member.alliance).order_by("-timestamp")[offset:offset+amount]
    ally_requests_list = [ally_request.to_dict() for ally_request in ally_requests]

    return build_success_response(
        ally_requests_list, HTTPStatus.OK, safe=False
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json(
    ("id", int)
)
def accept_ally_request(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role < AllianceRole.ADMIN:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    ally_request = AllianceAllyRequest.objects.filter(pk=id).first()

    if ally_request is None:
        return build_error_response(
            "The ally request does not exist!", HTTPStatus.BAD_REQUEST
        )
    
    AllianceAlly.objects.create(
        requester=ally_request.requesting_alliance,
        acceptor=ally_request.alliance
    )

    ally_request.delete()

    return build_success_response(
        "Successfully accepted ally request!", HTTPStatus.CREATED
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json(
    ("id", int)
)
def deny_ally_request(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role < AllianceRole.ADMIN:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    ally_request = AllianceAllyRequest.objects.filter(pk=id).first()

    ally_request.delete()

    return build_success_response(
        "Successfully denied ally request!", HTTPStatus.OK
    )

@needs_nation
@require_http_methods(["POST"])
@parse_json(
    ("id", int)
)
def declare_enemy(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None or alliance_member.role < AllianceRole.ADMIN:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    enemy_alliance = Alliance.objects.filter(pk=id).first()

    if enemy_alliance is None:
        return build_error_response(
            "The alliance does not exist!", HTTPStatus.BAD_REQUEST
        )
    
    existing_enemy = AllianceEnemy.objects.filter(enemy=enemy_alliance).first()

    if existing_enemy is not None:
        return build_error_response(
            "You are already enemies!", HTTPStatus.BAD_REQUEST
        )
    
    AllianceEnemy.objects.create(
        aggressor=alliance_member.alliance,
        enemy=enemy_alliance
    )

    return build_success_response(
        "Successfully created an enemy!", HTTPStatus.CREATED
    )

@needs_nation
@require_http_methods(["GET"])
@parse_json(
    ("page", int),
    ("amount", int),
    ("relation", str)
)
def get_alliance_relations(request: HttpRequest, page: int, amount: int, relation: str) -> JsonResponse:
    user: User = request.user
    nation: Nation = user.nation

    alliance_member = AllianceMember.objects.filter(nation=nation).first()

    if alliance_member is None:
        return build_error_response(
            "You are unauthorized to do this!", HTTPStatus.UNAUTHORIZED
        )
    
    offset = page * amount

    alliance: Alliance = alliance_member.alliance

    match relation:
        case "enemies":
            enemies = AllianceEnemy.objects.filter(aggressor=alliance)[offset:offset+amount]
            enemies_list = [enemy.enemy.to_dict() for enemy in enemies]

            return build_success_response(
                enemies_list, HTTPStatus.CREATED, safe=False
            )

        case "allies":
            allies = AllianceAlly.objects.filter(Q(requester=alliance) | Q(acceptor=alliance))[offset:offset+amount]
            allies_list = [ally.acceptor.to_dict() if ally.acceptor != alliance else ally.requester.to_dict() for ally in allies]

            return build_success_response(
                allies_list, HTTPStatus.CREATED, safe=False
            )
        
        case _:
            return build_error_response(
                "Unknown relation type!", HTTPStatus.BAD_REQUEST
            )

    return build_success_response(
        "Successfully created an enemy!", HTTPStatus.CREATED
    )