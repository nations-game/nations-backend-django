import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import User

@require_http_methods(["POST"])
def signup_user(request: HttpRequest) -> JsonResponse:
    if not request.body:
        return "" # Replace with error response later

    request_data: dict = json.loads(request.body)

    # Check if data is malformed or is wrong type
    try:
        username: str = request_data["username"]
        email: str = request_data["email"]
        password: str = request_data["password"]
        confirm_password: str = request_data["confirm_password"]
        accepted_tos: bool = request_data["accepted_tos"]
    except KeyError:
        return "" # Replace with malformed request error response later

    if not accepted_tos:
        return "" # Replace with tos acceptance error response later

    if password != confirm_password:
        return "" # Replace with password confirmation error response later
    
    user: User = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        nation=None
    )

    login(request, user)
    request.session.save()
    
    response: JsonResponse = JsonResponse({
        "status": "success",
        "details": user.to_dict()
    }, status=200)
    
    return response

@require_http_methods(["POST"])
def login_user(request: HttpRequest) -> JsonResponse:
    if not request.body:
        return "" # Replace with error response later

    request_data: dict = json.loads(request.body)
    
    email: str = request_data.get("email")
    password: str = request_data.get("password")

    user: User = authenticate(email=email, password=password)

    if not User:
        return "" # Replace with error response later
    
    login(request, user)
    request.session.save()

    return HttpResponse("hi mom!!")

@require_http_methods(["GET"])
def user_info(request: HttpRequest) -> JsonResponse:
    return HttpResponse("hi mom!!")

@require_http_methods(["GET"])
def test_sessions(request: HttpRequest) -> JsonResponse:
    user_name = request.user.get_username()

    return HttpResponse(user_name)