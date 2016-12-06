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

    quick_answers_dict = {}

    for qquestion in QQuestion.objects.all():
      for qvote in qquestion.qvote_set.filter(author=self.request.user):
        quick_answers_dict[qquestion] = qvote

    responses_exist = {}

    for question in questions:
      for response in question.response_set.filter(author=self.request.user):
        responses_exist [question] = True


    context['quick_answers'] = quick_answers_dict
    context['paged_object'] = questions
    context['num_of_not_answered'] = count_not_answered(self.request)
    context['responses_exist'] = responses_exist

    print (quick_answers_dict)

    return context

def diagrams(request):
  return render(request, 'overview/diagrams.html')



