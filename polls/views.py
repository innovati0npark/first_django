from django.http import HttpResponse, Http404
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from datetime import datetime

# def index(request):     
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]       #요청들어오면 Question 데이터를 정렬한다. 앞에서 5개 갖고온다.
#     template = loader.get_template("polls/index.html")                      #아까 polls에 저장한 html 연결
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))       
#디버그 모드에서 멈추려면 해당되는 주소로 요청보내면 됨.

def index(request):                                         #위 인덱스와 같은 내용인데 간소화한 표현.
    latest_question_list = Question.objects.order_by("-pub_date")[:10]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

# def index(request):                                         #연습문제2, 4(Question.objects.get(pub_date__year=current_year))
#     # current_day = datetime.now().day       /current_year = datetime.now().year
#     today_question_list = Question.objects.filter(pub_date__day=28)            #Question.objects.get(pub_date__day=28) 로 하면 됨 연습2
#     output = ",".join([q.question_text for q in today_question_list])
#     return HttpResponse(output)
    
    

#index1 만들고 index1.html 만들어서 Choice도 가져와보기

# def index1(request):
#     choice_list = Choice.objects.order_by("votes")[:5]
#     context = {"choice_list": choice_list}
#     return render(request, "polls/index1.html", context)

def index1(request):                                           #연습문제5
    choice_list = Choice.objects.filter(votes__gt=0)           #choice 내 votes가 0 이상인 경우만
    context = {"choice_list": choice_list}
    return render(request, "polls/index1.html", context)


# def index1(request):                                        #연습문제3
#     choice_list = Choice.objects.order_by("votes")[:5]
#     context = {"choice_list": choice_list}
#     # return render(request, "polls/index1.html", context)
#     return HttpResponse ("Hello World!")
        #HttpResponse 이걸로 안 감싸주면 HTTP 프로토콜 양식에 맞지 않아서 전송이 안됨.




# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")            #Question 없으면 404에러 발생
#     return render(request, "polls/detail.html", {"question": question}) #polls폴더에 detail.html 필요

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def innopark(request, question_text):
    return HttpResponse("You're voting on question %s." % question_text)
#question id 말고 다른 이름으로 받아도 될까?  > 안됨

#숫자가 아닌 게 들어오면 어떻게 됨 ?? >> question_text로 받을 수 있음.

