from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.urls import reverse, reverse_lazy
from django.views import generic

class QuestionCreateView(generic.edit.CreateView):
    model = Question
    fields = ['question_text', 'pub_date']
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('polls:index')  #   예시 URL, 실제 프로젝트에 맞게 수정 필요

class ChoiceCreateView(generic.edit.CreateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_form.html'
    
    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('polls:detail', kwargs={'question_id': self.kwargs['pk']})
    
    success_url = reverse_lazy('polls:index')

class QuestionUpdateView(generic.edit.UpdateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/question_update_form.html' 
    success_url = reverse_lazy('polls:index')  

class ChoiceUpdateView(generic.edit.UpdateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_update_form.html'  # 새로운 템플릿 또는 기존 템플릿 지정

    def get_success_url(self):
        # 선택지가 업데이트된 후, 선택지가 속한 질문의 상세 페이지로 리다이렉션
        choice = self.object
        return reverse('polls:detail', kwargs={'question_id': choice.question.pk})

class QuestionDeleteView(generic.edit.DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete.html'
    success_url = reverse_lazy('polls:index')  # 삭제 후 리다이렉션될 URL, 실제 프로젝트에 맞게 수정 필요


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
    context = {"latest_question_list": latest_question_list
               }
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
    question_list = Question.objects.all
    context = {
        "question": question, 
        "question_list": question_list
    }
    return render(request, "polls/detail.html", context)
#     return HttpResponse("""
#     <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Document</title>
# </head>
# <body>
#     <p>InnovationPARK</p>
#     <p>InnovationPARK</p>
#     <p>InnovationPARK</p>
# </body>
# </html>
#                         Hello""")

def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

# def vote(request, question_id):
    # choice 데이터에서 해당하는 값에다 votes를 1 더하기
    # c = Choice.objects.get(pk=3)
    # c.votes +=1
    # c.save()
    # return HttpResponse("You're voting on question %s." % question_id)


##Tutorial CODE F함수
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


# F함수가 속도가 훨씬 빠르다.
from django.db.models import F, Case, When, Value
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        #votes 값을 1 증가시키고 저장한다. (F함수 사용)
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        #votes 값을 1 증가시키고 저장한다. (F함수 미사용)
        # selected_choice.votes += 1
        # selected_choice.save()
        # 성공적으로 처리한 후 항상 HttpResponseRedirect를 반환.
        # POST data쓰면 데이터 두번 게시되는거 방지. 사용자가 단추 두 번 눌러도.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

#UPDATE 사용하는법
### Model.objects.filter(조건).update(필드1=값1, 필드2=값2, ...)

#F함수 연습문제1 (모든 선택지의 투표 수 1 증가)
# Choice.objects.all().update(votes = F("votes")+1)
    
#F함수 연습문제2 (특정 선택지의 투표 수 감소)
# Choice.objects.update(votes=Case(
#     When(votes__gt=0, then=F('votes') - 1),
#     default=Value(0)
# ))
#F함수 연습문제3 (특정 질문에 대한 모든 선택지의 투표를 두 배로 늘리기)
# Choice.objects.filter(votes__gt=0).update(votes=F('votes') * 2)

def innopark(request, question_text):
    return HttpResponse("You're voting on question %s." % question_text)
#question id 말고 다른 이름으로 받아도 될까?  > 안됨

#숫자가 아닌 게 들어오면 어떻게 됨 ?? >> question_text로 받을 수 있음.

from django.views import generic
from django.db.models import Sum

#IndexView
class IndexView(generic.ListView):
    #[app_name]/[model_name]_list.html > 보통 이런 형식의 경로를 씀.
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        # 1번 
        return Question.objects.order_by("-pub_date")[:]
        #2번 top_questions = Question.objects.annotate(total_votes=Sum('choice__votes')).order_by('-total_votes')[:5]
        #3번 
        unvoted_questions = Question.objects.annotate(total_votes=Sum('choice__votes')).filter(total_votes=0)
        return unvoted_questions
        

#DetailView
class DetailView(generic.DetailView):
    #self.kwargs는 url.py의 <int: ~> ~변수와 request숫자를 담는 딕셔너리.
    model = Question
    template_name = "polls/detail.html"
    def get_object(self):
        question_id = self.kwargs['question_id']
        question = get_object_or_404(Question, pk=question_id)
        return question
    



#ResultsView
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"