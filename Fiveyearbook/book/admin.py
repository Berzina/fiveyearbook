from django.contrib import admin
from book.models import Question, Response, QQuestion, QResponse

admin.site.register(Question)
admin.site.register(QQuestion)
admin.site.register(QResponse)