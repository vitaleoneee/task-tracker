from django.urls import path

from tasktracker.apps.tracker.views.common_views import DashboardView
from tasktracker.apps.tracker.views.project_views import (
    ProjectCreateView,
    ProjectListView,
    ProjectDeleteView,
    ProjectUpdateView,
    ProjectDetailView,
)
from tasktracker.apps.tracker.views.tasks_views import (
    TaskCreateView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
)

app_name = "tracker"
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    # Project urls
    path("project-list/", ProjectListView.as_view(), name="project_list"),
    path(
        "projects/<int:pk>/detail/", ProjectDetailView.as_view(), name="project_detail"
    ),
    path("add-project/", ProjectCreateView.as_view(), name="project_add"),
    path(
        "project-update/<int:pk>/", ProjectUpdateView.as_view(), name="project_update"
    ),
    path(
        "project-delete/<int:pk>/", ProjectDeleteView.as_view(), name="project_delete"
    ),
    # Task urls
    path("projects/<int:pk>/task-list/", TaskListView.as_view(), name="task_list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("projects/<int:pk>/add-task/", TaskCreateView.as_view(), name="task_add"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
]
