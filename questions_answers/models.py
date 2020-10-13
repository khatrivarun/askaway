from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    slug = models.SlugField(unique=True, null=False)
    question = models.TextField(null=False)
    votes = models.IntegerField(default=0, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    added = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True, null=False)

    objects = models.Manager()


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    answer = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    added = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True, null=False)

    objects = models.Manager()
