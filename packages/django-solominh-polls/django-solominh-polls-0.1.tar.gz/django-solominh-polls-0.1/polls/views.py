from django.shortcuts import render,get_object_or_404
from .models import Question,Choice
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic

# Create your views here.

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='questions'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DeleteView):
    template_name='polls/detail.html'
    model=Question

class ResultView(generic.DetailView):
    model=Question
    template_name='polls/result.html'

def index(request):
    latest_questions=Question.objects.order_by('pub_date')[:5]
    context = {'questions':latest_questions}
    return render(request, 'polls/index.html', context)

def detail(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    context={'question':question}
    return render(request,'polls/detail.html',context)

def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except:
        context={'question':question,
            'error_message':'Please choose a choice',
        }
        return render(request,'polls/detail.html',context)
    else:
        selected_choice.votes=F('votes') +1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result',args=(question_id,)))

def result(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    context={'question':question}
    return render(request,'polls/result.html',context)