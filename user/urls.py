from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/', signin),
    path('update/', update),
    path('update_password/', update_password),
    path('logout/', auth_views.LogoutView.as_view())
]
