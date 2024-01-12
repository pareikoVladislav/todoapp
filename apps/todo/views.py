from django.contrib.auth.models import User
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required

from apps.todo.forms import (
    CreateTaskForm,
    TaskUpdateForm,
    SubTaskUpdateForm,
    SubTaskCreateForm
)
from apps.todo.models import (
    Task,
    SubTask,
    Category,
    Status,
)


def home_page(request):
    return render(
        request=request,
        template_name='main.html',
    )


@login_required(login_url='router:user:login')
def get_all_tasks(request):
    tasks = Task.objects.filter(
        creator=request.user
    )

    context = {
        "tasks": tasks
    }

    return render(
        request=request,
        template_name='todo/all_tasks.html',
        context=context
    )


@login_required(login_url='router:user:login')
def create_new_task(request):
    user = get_object_or_404(User, id=request.user.id)
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
            "users": user,
            "categories": categories,
            "statuses": statuses
        }

    else:
        form = CreateTaskForm()
        context = {
            "form": form,
            "users": user,
            "categories": categories,
            "statuses": statuses
        }

    return render(
        request=request,
        template_name='todo/create_task.html',
        context=context
    )


@login_required(login_url='router:user:login')
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
            "task": task,
            "categories": categories,
            "statuses": statuses
        }
    else:
        form = TaskUpdateForm(instance=task)

        context = {
            "form": form,
            "task": task,
            "categories": categories,
            "statuses": statuses
        }

    return render(
        request=request,
        template_name='todo/update_task.html',
        context=context
    )


@login_required(login_url='router:user:login')
def get_task_info_by_task_id(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    subtasks = SubTask.objects.filter(
        task=task_id
    )

    context = {
        "task": task,
        "subtasks": subtasks
    }

    return render(
        request=request,
        template_name='todo/task_info.html',
        context=context
    )


@login_required(login_url='router:user:login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.delete()
    return redirect('router:tasks:all-tasks')


@login_required(login_url='router:user:login')
def get_subtasks_info(request):
    subtasks = SubTask.objects.filter(
        creator=request.user
    )

    context = {
        "subtasks": subtasks
    }

    return render(
        request=request,
        template_name='todo/all_subtasks.html',
        context=context
    )


@login_required(login_url='router:user:login')
def get_subtask_info_by_id(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    context = {
        "subtask": subtask
    }

    return render(
        request=request,
        template_name='todo/subtask_info.html',
        context=context
    )


@login_required(login_url='router:user:login')
def create_subtask(request):
    task_id = request.GET.get("task_id")

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()
    statuses = Status.objects.all()
    task = get_object_or_404(Task, id=task_id)

    form = SubTaskCreateForm()

    if request.method == 'POST':
        form = SubTaskCreateForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('router:tasks:task-info', task_id=task_id)

    context = {
        "form": form,
        "user": user,
        "categories": categories,
        "statuses": statuses,
        "task": task
    }

    return render(
        request=request,
        template_name='todo/create_subtask.html',
        context=context
    )


@login_required(login_url='router:user:login')
def update_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    categories = Category.objects.all()
    statuses = Status.objects.all()

    form = SubTaskUpdateForm(instance=subtask)

    if request.method == 'POST':
        form = SubTaskUpdateForm(request.POST, instance=subtask)

        if form.is_valid():
            form.save()

            return redirect('router:tasks:subtask-info', subtask_id=subtask_id)

    context = {
        "form": form,
        "subtask": subtask,
        "categories": categories,
        "statuses": statuses
    }

    return render(
        request=request,
        template_name='todo/update_subtask.html',
        context=context
    )


@login_required(login_url='router:user:login')
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    subtask.delete()
    return redirect('router:tasks:all-subtasks')
