from django.contrib import admin
from .models import Task, Tag, TaskTag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'deadline')
    search_fields = ('name', 'description')
    list_filter = ('date', 'deadline')
    ordering = ('-date',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(TaskTag)
class TaskTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'tag')
    list_filter = ('tag',)
    search_fields = ('task__name', 'tag__name')
    autocomplete_fields = ('task', 'tag')