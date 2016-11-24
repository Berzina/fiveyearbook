from django.conf.urls import url, include
from . import views
from django.views.generic import ListView, DetailView
from book.models import Question
from . import views

urlpatterns = [
  url(r'^$', ListView.as_view(queryset=Question.objects.all().order_by("date"),
                              template_name = "book/book.html")),
  # url(r'(?P<question_id>[0-9]+)/$', views.question)
      url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='question'),
      url(r'^(?P<question_id>[0-9]+)/response/$', views.response, name='response')]