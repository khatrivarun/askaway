from django.contrib import admin
from django.urls import path, include
from .views import landing

urlpatterns = [
    path('', landing),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('questions/', include('questions_answers.urls'))
]

handler404 = 'errors.views.page_not_found'
handler403 = 'errors.views.permission_denied'
handler400 = 'errors.views.bad_request'
handler500 = 'errors.views.error'
