from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from apps.todo.models import Task, SubTask
from apps.user.forms import LoginForm, CreateUserForm


def us_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(
                request=request,
                username=username,
                password=password
            )

            if user is not None:
                auth.login(request, user=user)

                return redirect('router:tasks:all-tasks')

    context = {
        "form": form
    }

    return render(
        request=request,
        template_name='user/login.html',
        context=context
    )


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('router:user:login')

    context = {
        "form": form
    }

    return render(
        request=request,
        template_name='user/register.html',
        context=context
    )


@login_required(login_url='router:user:login')
def us_info(request):
    user = get_object_or_404(User, id=request.user.id)
    tasks = Task.objects.filter(
        creator=user.id
    )
    subtasks = SubTask.objects.filter(
        creator=user.id
    )

    context = {
        "user": user,
        "tasks": tasks,
        "subtasks": subtasks
    }

    return render(
        request=request,
        template_name='user/profile.html',
        context=context
    )


@login_required(login_url='router:user:login')
def us_logout(request):
    auth.logout(request=request)
    return redirect('router:user:login')
