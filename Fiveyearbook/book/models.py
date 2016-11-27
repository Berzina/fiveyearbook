from django.db import models

class Question(models.Model):
  title = models.CharField(max_length=140)
  date = models.DateTimeField()

  def __str__(self):
    return self.title

class Response(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  text = models.CharField(max_length=140)
  date = models.DateTimeField()

  def __str__(self):
    return self.text

class Comment(models.Model):
  question = models.ForeignKey(Response, on_delete=models.CASCADE)
  text = models.CharField(max_length=140)
  date = models.DateTimeField()

  def __str__(self):
    return self.text

class QQuestion(models.Model):
  title = models.CharField(max_length=140)
  date = models.DateTimeField()

  def __str__(self):
    return self.title

class QResponse(models.Model):
  qquestion = models.ForeignKey(QQuestion, on_delete=models.CASCADE)
  text = models.CharField(max_length=140)
  date = models.DateTimeField()
  vote = models.IntegerField()

  def __str__(self):
    return self.text
