from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasktracker.apps.tracker.urls")),
    path("auth/", include("tasktracker.apps.users.urls")),
]
