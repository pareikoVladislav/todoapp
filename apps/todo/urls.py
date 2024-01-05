from django.urls import path
from apps.todo.views import (
    get_all_tasks,
    create_new_task,
    update_task,
    get_task_info_by_task_id,
    delete_task
)

app_name = "tasks"

urlpatterns = [
    path("", get_all_tasks, name='all-tasks'),
    path("create/", create_new_task, name='create-task'),
    path("<int:task_id>/", get_task_info_by_task_id, name='task-info'),
    path("<int:task_id>/update/", update_task, name='update-task'),
    path("<int:task_id>.delete/", delete_task, name='delete-task'),
]
