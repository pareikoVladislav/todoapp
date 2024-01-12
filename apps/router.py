from django.urls import path, include
from apps.todo.views import home_page

app_name = 'router'

urlpatterns = [
    path("", home_page, name='home'),
    path("tasks/", include('apps.todo.urls')),
    path("user/", include('apps.user.urls'))
]
