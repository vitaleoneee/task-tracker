from django.urls import path

from tasktracker.apps.tracker.views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
]
