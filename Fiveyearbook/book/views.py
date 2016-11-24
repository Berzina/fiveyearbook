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

  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))