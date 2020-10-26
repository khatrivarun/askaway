from django.contrib import admin
from .models import Question, Answer, Vote

# Registering the models with the admin.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Vote)
