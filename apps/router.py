from django.urls import path, include

urlpatterns = [
    path("tasks/", include('apps.todo.urls'))
]
