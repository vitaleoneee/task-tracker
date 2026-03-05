from django.contrib import admin
from tasktracker.apps.tracker.models import (
    Project,
    Task,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner__username")
    list_filter = ("created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "is_completed", "priority", "due_date")
    search_fields = ("title", "project__name")
    list_filter = ("is_completed", "priority", "due_date")
