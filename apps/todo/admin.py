from django.contrib import admin

from apps.todo.models import (
    Task,
    SubTask,
    Status,
    Category
)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'creator', 'created_at')
    list_filter = ('category', 'status', 'creator', 'created_at')
    search_fields = ('title',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    def change_subtasks_register(self, request, queryset):
        for obj in queryset:
            obj.title = obj.title.upper()
            obj.save()

    change_subtasks_register.short_description = 'Up register'

    actions = [
        'change_subtasks_register',
    ]

    list_display = ('title', 'category', 'task', 'status', 'creator', 'created_at')
    list_filter = ('task', 'category', 'status', 'creator', 'created_at')
    search_fields = ('title',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

