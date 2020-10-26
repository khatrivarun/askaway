from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

# User Routes
urlpatterns = [
    path('register/', register),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html')),
    path('me/', view_me),
    path('view/<str:username>', view_user),
    path('update/', update),
    path('update_password/', update_password),
    path('delete/', delete_account),
    path('logout/', auth_views.LogoutView.as_view())
]
