import json
from django.shortcuts import redirect
from django.http import JsonResponse, HttpRequest
from .utils import validate_dict_types, build_error_response
from .models import User

def parse_json(*type_list: tuple[str, object]):
    def decorator(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            try:
                try:
                    body_dict = json.loads(request.body)
                except:
                    body_dict = dict(request.POST)

                if "csrfmiddlewaretoken" in body_dict:
                    del body_dict["csrfmiddlewaretoken"]

                for key, value in body_dict.items():
                    if isinstance(value, list) and len(value) == 1:
                        body_dict[key] = value[0]

                # Check that dict types are valid and that extra data is not passed
                if not validate_dict_types(body_dict, type_list) or len(body_dict) > len(type_list):
                    raise Exception
                
                func_arguments = [body_dict[t[0]] for t in type_list]
            except Exception as e:
                return build_error_response(
                    "Malformed Request", 400
                )
            
            return view_func(request, *args, *func_arguments, **kwargs)

        return wrapper
    return decorator

def needs_auth(view_func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return build_error_response(
                "Not authenticated!", 401
            )
        
        return view_func(request, *args, **kwargs)
    return wrapper

def needs_nation(view_func):
    @needs_auth # Using the decorator here as nation checking needs auth checking either way
    def wrapper(request: HttpRequest, *args, **kwargs):
        user: User = request.user
        if user.nation is None:
            return build_error_response(
                "User does not have a nation!", 401
            )
        return view_func(request, *args, **kwargs)

    return wrapper

def needs_auth_frontend(view_func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return redirect("/app/login")
        
        return view_func(request, *args, **kwargs)
    return wrapper

def needs_nation_frontend(view_func):
    @needs_auth # Using the decorator here as nation checking needs auth checking either way
    def wrapper(request: HttpRequest, *args, **kwargs):
        user: User = request.user
        if user.nation is None:
            return redirect("/app/dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper