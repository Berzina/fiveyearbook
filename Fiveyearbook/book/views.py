from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Response, Question
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


# Create your views here.
class DetailView(generic.DetailView):
  model = Question
  template_name = 'book/question.html'

  def get_context_data(self, **kwargs):
    question = self.get_object()
    context = super(DetailView, self).get_context_data(**kwargs)

    response_list = question.response_set.all()
    paginator = Paginator(response_list.order_by('-date'), 5)
    page = self.request.GET.get('page',1)
    responses = paginator.page(page)

    # qquestion_list = question.qquestion_set.all()
    # paginator = Paginator(qquestion_list, 1)
    # page = self.request.GET.get('view',1)
    # qquestions = paginator.page(page)
    #
    # page = self.request.GET.get('page',1)
    # view = self.request.GET.get('view',1)

    # Are you able to answer the question?
    # 
    # 1. Question should have date which is current or + 7days
    current_date = timezone.now()

    timedelta = current_date - question.date

    if timedelta.days >= 0 and timedelta.days <= 7:
      context ["current_week"] = True
    else:
      context ["current_week"] = False

    # 2. Question should not have answers this year
    # 
    if not question.response_set.filter(date__year = timezone.now().year):        
      context ["main_not_answered"] = True
    else:
      context ["main_not_answered"] = False

    # 3. Question should not have answers this day:
    #
    for qquestion in QQuestion.objects.all():
      if not qquestion.qresponse_set.filter(date__month = timezone.now().year, date__day = timezone.now().day):
        context [ str(qquestion.id) + "_not_answered" ] = True
      else:
        context [ str(qquestion.id) + "_not_answered" ] = False

    context["current_day"] = True
    context['paged_object'] = responses
    context['quick_questions'] = QQuestion.objects.all()

    return context




class ListView(generic.ListView):
  model = Question
  template_name = "book/book.html"

  def get_context_data(self, **kwargs):

    question_list = Question.objects.all()
    paginator = Paginator(question_list.order_by('-date'), 3)
    context = super(ListView, self).get_context_data(**kwargs)
    page = self.request.GET.get('page',1)
    questions = paginator.page(page)

    context['paged_object'] =  questions
    return context 


def response(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  response_text = request.POST['response']
  comment_text = request.POST['comment']

  if response_text:
    response = question.response_set.create(text=response_text, date=timezone.now())
  else:
    messages.error(request, "Вы должны ввести ответ на вопрос!")

  if comment_text:
    comment = response.comment_set.create(text=comment_text, date=timezone.now())

  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def comment(request, response_id):

  response = get_object_or_404(Response, pk=response_id)
  text = request.POST['comment']

  if text:
    comment = response.comment_set.create(text=text, date=timezone.now())
  else:
    messages.warning(request, "Вы ничего не ввели, коммент не добавлен")

  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def vote(request, qquestion_id):

  question = get_object_or_404(QQuestion, pk=qquestion_id)

  try:
    choice = request.POST['choice']
  except:
    messages.warning(request, "Вы не ответили на вопрос.")
  else:
    selected_choice = question.qvote_set.create(date=timezone.now(), vote=choice)

  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))