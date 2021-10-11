from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse


def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello")
