from django.urls import path

from tasktracker.apps.tracker.views import DashboardView

app_name = "tracker"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
]
