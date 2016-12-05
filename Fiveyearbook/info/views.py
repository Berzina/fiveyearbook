from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views import generic

from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import authenticate

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


  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def index(request):

  return render(request, 'info/home.html')
