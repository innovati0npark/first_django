from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def cafe_menu(request):
    return HttpResponse("우리 맛집이에요 !")

def order_coffee(request):
    return HttpResponse("피스타치오 아미레카노 주세요!")

def innopark(request):
    return HttpResponse("InnovationPARK here!")