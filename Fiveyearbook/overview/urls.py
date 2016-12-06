from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.ListView.as_view(), name='overview'),
  url(r'^diagrams/$', views.diagrams, name='diagrams')
  ]