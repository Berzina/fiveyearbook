from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Response, Question, QQuestion, QVote
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

    quick_not_answered_dict = {}
    for qquestion in QQuestion.objects.all():
      if not qquestion.qvote_set.filter(date__month = timezone.now().month, date__day = timezone.now().day):
        quick_not_answered_dict [ qquestion ] = True
      else:
        quick_not_answered_dict [ qquestion ] = False

    quick_answers_dict ={}

    for qquestion in QQuestion.objects.all():
      for qvote in qquestion.qvote_set.filter(date__month=timezone.now().month, date__day=timezone.now().day):
        quick_answers_dict[qquestion] = qvote
        print (type(qvote.vote))

    context['paged_object'] = responses
    context['quick_questions'] = QQuestion.objects.all()
    context['quick_not_answered'] = quick_not_answered_dict
    context['quick_answers'] = quick_answers_dict

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
  variant_title =question.variant1


  try:
    choice = request.POST['choice']
    if int(choice) == 3:
      variant_title = question.variant1
    elif int(choice) == 2:
      variant_title = question.variant2
    elif int(choice) == 1:
      variant_title = question.variant3

    selected_choice = question.qvote_set.create(date=timezone.now(), vote=choice, title=variant_title)
  except:
    messages.warning(request, "Вы не ответили на вопрос.")

  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))