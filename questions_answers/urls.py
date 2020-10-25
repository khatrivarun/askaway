from django.urls import path
from .views import *

urlpatterns = [
    path('question/<str:slug>/', list_single_question),
    path('question/<str:slug>/update/', update_single_question),
    path('create/', create_question)
]
