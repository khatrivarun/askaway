from django.urls import path
from .views import *

# All required URLs.
urlpatterns = [
    path('all/', list_questions),
    path('question/<str:slug>/', list_single_question),
    path('question/<str:slug>/noice/<int:answer_id>/', vote),
    path('question/<str:slug>/update/', update_single_question),
    path('question/<str:slug>/answer/', create_answer),
    path('question/<str:slug>/answer/<int:answer_id>/delete/', delete_answer),
    path('create/', create_question)
]
