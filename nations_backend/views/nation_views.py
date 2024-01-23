from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest ,JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def create_nation(request: HttpRequest) -> JsonResponse:
    return HttpResponse("hi mom!!")

@require_http_methods(["POST"])
def nation_info(request: HttpRequest) -> JsonResponse:
    return HttpResponse("hi mom!!")

@require_http_methods(["GET"])
def nation_factories(request: HttpRequest) -> JsonResponse:
    return HttpResponse("hi mom!!")