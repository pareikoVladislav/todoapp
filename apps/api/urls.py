from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.api.views import (
    # task_list,
    # create_new_task,
    TasksApiView,
    TaskDetailGenericView,
    StatusViewSet,
    CategoryViewSet
)

router = DefaultRouter()

router.register(r'status', StatusViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    # path("tasks/", task_list),
    # path("task-create/", create_new_task)
    path("tasks/", TasksApiView.as_view()),
    path("task/<int:task_id>/", TaskDetailGenericView.as_view()),
] + router.urls
