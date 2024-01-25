import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import User
from ..utils import validate_dict_types

@require_http_methods(["POST"])
def signup_user(request: HttpRequest) -> JsonResponse:
    if not request.body:
        return JsonResponse({
            "status": "error",
            "details": "Malformed request."
        }, status=400)

    request_data: dict = json.loads(request.body)

    # Check if data is malformed or is wrong type
    is_valid = validate_dict_types(request_data, [
        ("username", str),
        ("email", str),
        ("password", str),
        ("confirm_password", str),
        ("accepted_tos", bool),
    ])

    if not is_valid:
        return JsonResponse({
            "status": "error",
            "details": "Malformed request."
        }, status=400)

    username: str = request_data["username"]
    email: str = request_data["email"]
    password: str = request_data["password"]
    confirm_password: str = request_data["confirm_password"]
    accepted_tos: bool = request_data["accepted_tos"]

    if not accepted_tos:
        return JsonResponse({
            "status": "error",
            "details": "Please accept the Terms of Service!"
        }, status=400)

    if password != confirm_password:
        return JsonResponse({
            "status": "error",
            "details": "Passwords do not match!"
        }, status=400)
    
    user: User = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        nation=None
    )

    login(request, user)
    request.session.save()
    
    return JsonResponse({
        "status": "success",
        "details": user.to_dict()
    }, status=200)

@require_http_methods(["POST"])
def login_user(request: HttpRequest) -> JsonResponse:
    if not request.body:
        return JsonResponse({
            "status": "error",
            "details": "Malformed request."
        }, status=400)

    request_data: dict = json.loads(request.body)

    is_valid = validate_dict_types(request_data, [
        ("email", str),
        ("password", str),
    ])

    if not is_valid:
        return JsonResponse({
            "status": "error",
            "details": "Malformed request."
        }, status=400)
    
    email: str = request_data.get("email")
    password: str = request_data.get("password")

    user: User = authenticate(email=email, password=password)

    if not User:
        return JsonResponse({
            "status": "error",
            "details": "Could not find user!"
        }, status=404)
    
    login(request, user)
    request.session.save()

    return JsonResponse({
        "status": "success",
        "details": "Logged in."
    }, status=200)

@require_http_methods(["GET"])
def user_info(request: HttpRequest, username: str) -> JsonResponse:
    if request.user is None:
        return JsonResponse({
            "status": "error",
            "details": "Not authenticated!"
        }, status=401)
    
    if username == "me":
        user: User = request.user
    else:
        user: User = User.objects.filter(username=username).first()

    if user is None:
        return JsonResponse({
            "status": "error",
            "details": "Invalid user!"
        }, status=404)

    return JsonResponse(user.to_dict())