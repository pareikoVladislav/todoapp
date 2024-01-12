from django.contrib.auth.models import User
from django.forms import (
    ModelForm,
    fields,
    ModelChoiceField,
    widgets,
)

from apps.todo.models import (
    Category,
    Status,
    Task,
    SubTask
)


class CreateTaskForm(ModelForm):
    title = fields.CharField(max_length=25)
    description = fields.CharField(max_length=1500, widget=fields.Textarea)
    creator = ModelChoiceField(queryset=User.objects.all())
    category = ModelChoiceField(
        queryset=Category.objects.all(),
        required=False
    )
    status = ModelChoiceField(queryset=Status.objects.all())

    date_started = fields.DateField(
        widget=widgets.DateInput(attrs={"type": "data"})
    )
    deadline = fields.DateField(
        widget=widgets.DateInput(attrs={"type": "data"})
    )

    class Meta:
        model = Task
        fields = '__all__'


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'category', 'status', 'deadline')


class SubTaskCreateForm(ModelForm):
    class Meta:
        model = SubTask
        fields = [
            'title',
            'description',
            'category',
            'task',
            'status',
            'creator',
            'date_started',
            'deadline'
        ]


class SubTaskUpdateForm(ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'description', 'category', 'status', 'deadline']
