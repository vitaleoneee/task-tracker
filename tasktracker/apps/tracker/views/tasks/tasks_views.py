from django.http import HttpResponse
from django.views.generic import CreateView

from tasktracker.apps.tracker.models import Task, Project


class TaskCreateView(CreateView):
    model = Task
    template_name = "tracker/partials/tasks/create_task.html"
    fields = ["title", "due_date", "priority"]

    def form_valid(self, form):
        form.instance.project_id = self.kwargs["pk"]
        self.object = form.save()
        response = HttpResponse()
        response["HX-Trigger"] = "refreshData"
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(pk=self.kwargs["pk"])
        return context
