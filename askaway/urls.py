from django.contrib import admin
from django.urls import path, include
from .views import landing

urlpatterns = [
    path('', landing),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('questions/', include('questions_answers.urls'))
]
