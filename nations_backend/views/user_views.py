import json
from http import HTTPStatus

from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from ..decorators import parse_json, needs_auth
from ..models import User
from ..utils import build_error_response, build_success_response

@require_http_methods(["POST"])
@parse_json([
    ("username", str),
    ("email", str),
    ("password", str),
    ("confirm_password", str),
    ("accepted_tos", bool),
])
def signup_user(request: HttpRequest, username: str, email: str, password: str, confirm_password: str, accepted_tos: bool) -> JsonResponse:
    if not accepted_tos:
        return build_error_response(
            "Please accept the Terms of Service!", HTTPStatus.BAD_REQUEST
        )
    
    if password != confirm_password:
        return build_error_response(
            "Passwords do not match!", HTTPStatus.BAD_REQUEST
        )
    
    user: User = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        nation=None
    )

    login(request, user)
    request.session.save()
    
    return build_success_response(
        user.to_dict(), HTTPStatus.CREATED
    )

@require_http_methods(["POST"])
@parse_json([
    ("email", str),
    ("password", str),
])
def login_user(request: HttpRequest, email: str, password: str) -> JsonResponse:
    user: User = authenticate(email=email, password=password)

    if not User:
        return build_error_response(
            "Invalid Credentials", HTTPStatus.UNAUTHORIZED
        )
    
    login(request, user)
    request.session.save()
    
    return build_success_response(
        "Logged in", HTTPStatus.OK
    )

@require_http_methods(["GET"])
@needs_auth
def user_info(request: HttpRequest, username: str) -> JsonResponse:
    if username == "me":
        user: User = request.user
    else:
        user: User = User.objects.filter(username=username).first()

    if user is None:
        return build_error_response(
            "Invalid User", HTTPStatus.NOT_FOUND
        )

    return build_success_response(
        user.to_dict(), HTTPStatus.OK
    )