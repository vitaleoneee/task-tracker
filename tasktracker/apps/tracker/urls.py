from django.urls import path

from tasktracker.apps.tracker.views.common_views import DashboardView
from tasktracker.apps.tracker.views.projects.project_views import (
    ProjectCreateView,
    ProjectListView,
    ProjectDeleteView,
    ProjectUpdateView,
    ProjectDetailView,
)
from tasktracker.apps.tracker.views.tasks.tasks_views import (
    TaskCreateView,
    TaskListView,
    TaskUpdateView,
)

app_name = "tracker"
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    # Projects urls
    path("add-project/", ProjectCreateView.as_view(), name="add_project"),
    path("project-list/", ProjectListView.as_view(), name="project_list"),
    path(
        "project-update/<int:pk>/", ProjectUpdateView.as_view(), name="project_update"
    ),
    path(
        "project-delete/<int:pk>/", ProjectDeleteView.as_view(), name="project_delete"
    ),
    path(
        "projects/<int:pk>/detail/", ProjectDetailView.as_view(), name="project_detail"
    ),
    # Tasks urls
    path("projects/<int:pk>/task-list/", TaskListView.as_view(), name="task_list"),
    path("projects/<int:pk>/add-task/", TaskCreateView.as_view(), name="add_task"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
]
