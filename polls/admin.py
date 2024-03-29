from django.contrib import admin
from .models import Question, Choice                    #현 위치에 있는 models로부터
# Register your models here.

admin.site.register(Question)           #admin site에 question 등록
admin.site.register(Choice)