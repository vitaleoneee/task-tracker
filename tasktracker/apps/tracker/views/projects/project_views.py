from django.http import HttpResponse
from django.views.generic import CreateView

from tasktracker.apps.tracker.models import Project


class ProjectCreateView(CreateView):
    model = Project
    template_name = "tracker/partials/projects/create_project.html"
    fields = ["name"]
    success_url = "tracker:dashboard"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        response = HttpResponse()
        # Return an HTMX response to trigger the modal close
        response["HX-Trigger"] = "closeModal"
        return response
