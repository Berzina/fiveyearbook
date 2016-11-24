from django.conf.urls import url, include
from . import views
from django.views.generic import ListView, DetailView
from book.models import Question
from . import views

urlpatterns = [
  url(r'^$', views.ListView.as_view(), name='question_list'),
  # url(r'(?P<question_id>[0-9]+)/$', views.question)
      url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='question'),
      url(r'^(?P<question_id>[0-9]+)/response/$', views.response, name='response')]