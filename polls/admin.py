from django.contrib import admin
from .models import Question, Choice                    #현 위치에 있는 models로부터
# Register your models here.




class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3               #여분의 빈칸생기는거




class QuestionAdmin(admin.ModelAdmin):
    # fields = ["pub_date", "question_text"]
    fieldsets = [
        ("Question_index", {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines=[ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

# admin.site.register(Question)           #admin site에 question 등록
admin.site.register(Question, QuestionAdmin)


# admin.site.register(Choice)