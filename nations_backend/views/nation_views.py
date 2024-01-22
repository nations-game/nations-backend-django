from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def create(request: HttpRequest):
    return HttpResponse("hi mom!!")

@require_http_methods(["POST"])
def info(request: HttpRequest):
    return HttpResponse("hi mom!!")

@require_http_methods(["GET"])
def factories(request: HttpRequest):
    return HttpResponse("hi mom!!")