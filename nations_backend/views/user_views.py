import json
import time
from http import HTTPStatus

from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from ..decorators import parse_json, needs_auth
from ..models import User, Notification, Message
from ..utils import build_error_response, build_success_response

@require_http_methods(["POST"])
@parse_json(
    ("username", str),
    ("email", str),
    ("password", str),
    ("confirm_password", str),
    ("accepted_tos", bool),
)
def signup_user(request: HttpRequest, username: str, email: str, password: str, confirm_password: str, accepted_tos: bool) -> JsonResponse:
    if not accepted_tos:
        return build_error_response(
            "Please accept the Terms of Service!", HTTPStatus.BAD_REQUEST
        )
    
    if password != confirm_password:
        return build_error_response(
            "Passwords do not match!", HTTPStatus.BAD_REQUEST
        )
    
    try:
        user: User = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            nation=None
        )
    except IntegrityError:
        return build_error_response(
            "Username is not available!", HTTPStatus.BAD_REQUEST
        )

    login(request, user)
    request.session.save()
    
    return build_success_response({ 
        "sessionID": request.session.session_key,
        "maxAge": request.session.get_expiry_age(),
        "user": user.to_dict()
    }, HTTPStatus.CREATED)

@require_http_methods(["POST"])
@parse_json(
    ("username", str),
    ("password", str),
)
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
@parse_json(
    ("id", int)
)
def read_notification(request: HttpRequest, id: int) -> JsonResponse:
    notif = Notification.objects.filter(id=id).first()
    notif.read = True
    notif.save()

    return build_success_response(
        "Marked notification as read.", HTTPStatus.OK
    )

@require_http_methods(["POST"])
@needs_auth
@parse_json(
    ("subject", str),
    ("text", str),
    ("recipient_id", int),
)
def send_message(request: HttpRequest, subject: str, text: str, recipient_id: int) -> JsonResponse:
    user: User = request.user
    recipient = User.objects.filter(id=recipient_id).first()

    if recipient is None:
        return build_error_response(
            "Recipient does not exist!", HTTPStatus.BAD_REQUEST
        )
    
    if recipient == user:
        return build_error_response(
            "You cannot send messages to yourself!", HTTPStatus.BAD_REQUEST
        )
    
    try:
        Message.objects.create(
            sender=user,
            recipient=recipient,
            subject=subject,
            text=text,
            timestamp=time.time()
        )
    except IntegrityError:
        return build_error_response(
            "There was an error sending your message.", HTTPStatus.BAD_REQUEST
        )

    return build_success_response(
        "Succesfully sent message to user!", HTTPStatus.OK
    )

@require_http_methods(["GET"])
@needs_auth
@parse_json(
    ("page", int),
    ("amount", int)
)
def get_inbox(request: HttpRequest, page: int, amount: int) -> JsonResponse:
    user: User = request.user
    
    offset = page * amount
    msgs = Message.objects.filter(recipient=user).order_by("-timestamp")[offset:offset+amount]
    msgs_list = [msg.to_short_dict() for msg in msgs]

    return build_success_response(
        msgs_list, HTTPStatus.OK, safe=False
    )

@require_http_methods(["GET"])
@needs_auth
@parse_json(
    ("page", int),
    ("amount", int)
)
def get_sent_messages(request: HttpRequest, page: int, amount: int) -> JsonResponse:
    user: User = request.user

    offset = page * amount
    msgs = Message.objects.filter(sender=user).order_by("-timestamp")[offset:offset+amount]
    msgs_list = [msg.to_short_dict() for msg in msgs]

    return build_success_response(
        msgs_list, HTTPStatus.OK, safe=False
    )

@require_http_methods(["GET"])
@needs_auth
@parse_json(
    ("id", int),
)
def get_message(request: HttpRequest, id: int) -> JsonResponse:
    user: User = request.user

    msg = Message.objects.filter(Q(recipient=user) | Q(sender=user), id=id).first()

    if msg is None:
        return build_error_response(
            "Message does not exist!", HTTPStatus.BAD_REQUEST
        )

    return build_success_response(
        msg.to_dict(), HTTPStatus.OK
    )

def send_system_message(self, recipient_id: int, subject: str, text: str) -> None:
    recipient = User.objects.filter(id=recipient_id).first()

    if not recipient: return

    Message.objects.create(
        sender=None,
        recipient=recipient,
        subject=subject,
        text=text,
        timestamp=time.time()
    )
