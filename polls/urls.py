#polls 폴더에 urls.py가 없어서 새로 생성

from django.urls import path

from . import views


urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),            #polls 뒤 아무말 없는경우
    
    # ex: /polls/index1
    path("index1", views.index1, name="index1"),
    
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    
    path("<str:question_text>/innopark/", views.innopark, name="innopark"),

]