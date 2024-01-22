import json

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods

from ..models import User

@require_http_methods(["POST"])
def signup(request: HttpRequest) -> HttpResponse:
    if not request.body:
        return "" # Replace with error response later

    request_data: dict = json.loads(request.body)

    username: str = request_data.get("username")
    email: str = request_data.get("email")
    password: str = request_data.get("password")
    confirm_password: str = request_data.get("confirm_password")
    accepted_tos: bool = request_data.get("accepted_tos")

    if not accepted_tos:
        return "" # Replace with error response later

    if password != confirm_password:
        return "" # Replace with error response later
    
    user: User = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return HttpResponse("hi mom!!")

@require_http_methods(["POST"])
def login(request: HttpRequest) -> HttpResponse:
    if not request.body:
        return "" # Replace with error response later

    request_data: dict = json.loads(request.body)
    
    email: str = request_data.get("email")
    password: str = request_data.get("password")

    user: User = authenticate(email=email, password=password)
    
    if not User:
        return "" # Replace with error response later
    
    return login(request, user)

@require_http_methods(["GET"])
def user_data(request: HttpRequest) -> HttpResponse:
    return HttpResponse("hi mom!!")