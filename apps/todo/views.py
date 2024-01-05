from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from apps.todo.forms import CreateTaskForm, TaskUpdateForm
from apps.todo.models import (
    Task,
    Category,
    Status,
)


def home_page(request):
    return render(
        request=request,
        template_name='main.html',
    )


def get_all_tasks(request):
    tasks = Task.objects.all()

    context = {
        "tasks": tasks
    }

    return render(
        request=request,
        template_name='todo/all_tasks.html',
        context=context
    )


def create_new_task(request):
    users = User.objects.all()
    categories = Category.objects.all()
    statuses = Status.objects.all()

    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task_data = form.cleaned_data
            Task.objects.create(**task_data)
            return redirect('router:tasks:all-tasks')

        context = {
            "form": form,
            "users": users,
            "categories": categories,
            "statuses": statuses
        }

    else:
        form = CreateTaskForm()
        context = {
            "form": form,
            "users": users,
            "categories": categories,
            "statuses": statuses
        }

    return render(
        request=request,
        template_name='todo/create_task.html',
        context=context
    )


def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    categories = Category.objects.all()
    statuses = Status.objects.all()

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('router:tasks:all-tasks')

        context = {
            "form": form,
            "categories": categories,
            "statuses": statuses
        }
    else:
        form = TaskUpdateForm(instance=task)

        context = {
            "form": form,
            "categories": categories,
            "statuses": statuses
        }

    return render(
        request=request,
        template_name='todo/update_task.html',
        context=context
    )


def get_task_info_by_task_id(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    context = {
        "task": task
    }

    return render(
        request=request,
        template_name='todo/task_info.html',
        context=context
    )


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.delete()
    return redirect('router:tasks:all-tasks')
