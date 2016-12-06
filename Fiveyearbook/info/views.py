from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views import generic

from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from book.views import count_not_answered

def register (request):


  username = request.POST['username']
  email = request.POST['email']
  password = request.POST['password']
  confirm_password = request.POST['confirm-password']

  new_user = User.objects.create_user(username, email, password)


  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def login (request):

  print (request.POST)
  username = request.POST.get("username_login", False)
  password = request.POST.get("password_login", False)
  user = authenticate(username=username, password=password)
  login_django(request, user)


  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def index(request):

  if request.user.is_authenticated:
    context = {'user_logged': 'true',
               'username' : request.user.username,
               'num_of_not_answered': count_not_answered(request)}
  else:
    context = {'user_logged': 'false',
               'username' : request.user.username,
               'num_of_not_answered': count_not_answered(request)}

  return render(request, 'info/home.html', context)

def logout (request):

  logout_django(request)

  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))