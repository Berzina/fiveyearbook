from book.models import Question, QQuestion
from book.views import count_not_answered
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


class ListView(generic.ListView):
  model = Question
  template_name = "overview/main.html"

  def get_context_data(self, **kwargs):

    question_list = Question.objects.all()
    paginator = Paginator(question_list.order_by('-date'), 4)
    context = super(ListView, self).get_context_data(**kwargs)
    page = self.request.GET.get('page',1)
    questions = paginator.page(page)

    context['paged_object'] = questions
    context['num_of_not_answered'] = count_not_answered()

    return context

def diagrams(request):
  return render(request, 'overview/diagrams.html')
