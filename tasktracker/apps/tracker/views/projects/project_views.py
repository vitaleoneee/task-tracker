import json

from django.http import HttpResponse
from django.views.generic import (
    CreateView,
    ListView,
    DeleteView,
    UpdateView,
    DetailView,
)

from tasktracker.apps.tracker.models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "tracker/partials/projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "tracker/partials/projects/project_item.html"
    context_object_name = "project"


class ProjectCreateView(CreateView):
    model = Project
    template_name = "tracker/partials/projects/create_project.html"
    fields = ["name"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        response = HttpResponse()
        # Return an HTMX response to trigger the modal close and update the project list
        response["HX-Trigger"] = json.dumps({"closeModal": True, "refreshData": True})
        return response


class ProjectDeleteView(DeleteView):
    model = Project

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = HttpResponse()
        # Return an HTMX response to trigger the project list refresh
        response["HX-Trigger"] = "refreshData"
        return response


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = "tracker/partials/projects/update_project.html"
    fields = ["name"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        response = HttpResponse()
        # Return an HTMX response to trigger the project list refresh
        response["HX-Trigger"] = "refreshData"
        return response
