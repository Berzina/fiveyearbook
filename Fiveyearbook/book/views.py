from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Response, Question
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
class DetailView(generic.DetailView):
  model = Question
  template_name = 'book/question.html'

  def get_context_data(self, **kwargs):
    question = self.get_object()
    context = super(DetailView, self).get_context_data(**kwargs)

    response_list = question.response_set.all()
    paginator = Paginator(response_list, 5)
    page = self.request.GET.get('page',1)
    responses = paginator.page(page)

    # Are you able to answer the question?
    # 
    # 1. Question should have date which is current or + 7days
    current_date = timezone.now()

    timedelta = current_date - question.date
    
    if timedelta.days >= 0 and timedelta.days <= 7:
      context ["current_day"] = True
    else:
      context ["current_day"] = False

    # 2. Question should not have answers this year
    # 
    if not question.response_set.filter(date__year = timezone.now().year):        
      context ["not_answered"] = True
    else:
      context ["not_answered"] = False


    context['paged_object'] =  responses
    return context




class ListView(generic.ListView):
  model = Question
  template_name = "book/book.html"

  def get_context_data(self, **kwargs):

    question_list = Question.objects.all()
    paginator = Paginator(question_list, 3)
    context = super(ListView, self).get_context_data(**kwargs)
    page = self.request.GET.get('page',1)
    questions = paginator.page(page)

    context['paged_object'] =  questions
    return context 


def response(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  response = question.response_set.create(text=request.POST['response'], date=timezone.now())

  comment = response.comment_set.create(text=request.POST['comment'], date=timezone.now())

  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def comment(request, response_id):

  response = get_object_or_404(Response, pk=response_id)
  comment = response.comment_set.create(text=request.POST['comment'], date=timezone.now())

  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))