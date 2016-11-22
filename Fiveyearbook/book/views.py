from django.shortcuts import render

# Create your views here.
def question(request, question_id):
  return render(request, 'book/home.html', {'question_id': question_id})