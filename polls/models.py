from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):           #model.Model 상속받음.
    question_text = models.CharField(max_length=200)    #문자열 필드 생성
    pub_date = models.DateTimeField("date published")   #날짜 필드 생성

    def __str__(self):
        return self.question_text+"_Question", self.pub_date
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def print_length(self):
        return print(len(self.question_text))
        
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
#매직매서드 > 클래스 출력했을 때 길이 비교하거나, 문자열 출력하거나 등등 특별한 기능 수행.
    
