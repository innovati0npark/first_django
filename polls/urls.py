#polls 폴더에 urls.py가 없어서 새로 생성

from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("cafe_menu", views.cafe_menu, name="cafe_menu"),
    path("order", views.order_coffee, name="order"),

]