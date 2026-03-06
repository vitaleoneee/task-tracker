import json

from django.http import HttpResponse
from django.views.generic import CreateView, ListView

from tasktracker.apps.tracker.models import Project


class ProjectCreateView(CreateView):
    model = Project
    template_name = "tracker/partials/projects/create_project.html"
    fields = ["name"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        response = HttpResponse()
        # Return an HTMX response to trigger the modal close and update the project list
        response["HX-Trigger"] = json.dumps({"closeModal": None, "refreshData": None})
        return response


class ProjectListView(ListView):
    model = Project
    template_name = "tracker/partials/projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
