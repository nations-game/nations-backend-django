import json
from http import HTTPStatus

from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from ..decorators import parse_json, needs_auth
from ..models import User, Notification
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
    
    return build_success_response({ 
        "sessionID": request.session.session_key,
        "maxAge": request.session.get_expiry_age(),
        "user": user.to_dict()
    }, HTTPStatus.CREATED)

@require_http_methods(["POST"])
@parse_json([
    ("username", str),
    ("password", str),
])
def login_user(request: HttpRequest, username: str, password: str) -> JsonResponse:
    user: User = authenticate(username=username, password=password)

    if user is None:
        return build_error_response(
           "Invalid Credentials", HTTPStatus.UNAUTHORIZED
        )
    
    login(request, user)
    request.session.save()
    
    return build_success_response({ 
            "sessionID": request.session.session_key,
            "maxAge": request.session.get_expiry_age()
        }, HTTPStatus.OK)

@require_http_methods(["GET"])
@needs_auth
def user_info(request: HttpRequest, username: str) -> JsonResponse:
    if username == "me":
        user: User = request.user
        user.post_notification(title="Test Notification", details="Hello! This is a test notification.")
    else:
        user: User = User.objects.filter(username=username).first()

    if user is None:
        return build_error_response(
            "Invalid User", HTTPStatus.NOT_FOUND
        )

    return build_success_response(
        user.to_dict(), HTTPStatus.OK
    )

@require_http_methods(["GET"])
@needs_auth
def get_notifications(request: HttpRequest) -> JsonResponse:
    user: User = request.user

    notifications = Notification.objects.filter(user=user)

    notification_list = [notif.to_dict() for notif in notifications]

    notification_list.sort(key=lambda x: x["timestamp"], reverse=True)
    return build_success_response(
        notification_list, HTTPStatus.OK, safe=False
    )

@require_http_methods(["POST"])
@needs_auth
@parse_json([
    ("id", int)
])
def read_notification(request: HttpRequest, id: int) -> JsonResponse:
    notif = Notification.objects.filter(id=id).first()
    notif.read = True
    notif.save()

    return build_success_response(
        "Marked notification as read.", HTTPStatus.OK
    )