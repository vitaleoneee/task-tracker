from django.urls import path

from tasktracker.apps.tracker.views.common_views import DashboardView
from tasktracker.apps.tracker.views.projects.project_views import (
    ProjectCreateView,
    ProjectListView,
    ProjectDeleteView,
)

app_name = "tracker"
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    # Projects urls
    path("add-project/", ProjectCreateView.as_view(), name="add_project"),
    path("project-list/", ProjectListView.as_view(), name="project_list"),
    path(
        "project-delete/<int:pk>/", ProjectDeleteView.as_view(), name="project_delete"
    ),
]
