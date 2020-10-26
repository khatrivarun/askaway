from django.db import models
from django.contrib.auth.models import User


# Question Relation
class Question(models.Model):
    slug = models.SlugField(unique=True, null=False)
    question = models.CharField(null=False, max_length=255)
    description = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    added = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True, null=False)

    objects = models.Manager()


# Answer Relation
class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    answer = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    added = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True, null=False)

    objects = models.Manager()


# Vote Relation.
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False)

    objects = models.Manager()
