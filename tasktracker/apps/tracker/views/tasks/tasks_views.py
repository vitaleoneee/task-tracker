from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)

from tasktracker.apps.tracker.models import Task, Project


class TaskListView(ListView):
    model = Task
    template_name = "tracker/partials/tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs["pk"])


class TaskDetailView(DetailView):
    model = Task
    template_name = "tracker/partials/tasks/task_item.html"
    context_object_name = "task"


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


class TaskUpdateView(UpdateView):
    model = Task
    template_name = "tracker/partials/tasks/update_task.html"
    fields = ["title", "due_date", "priority"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "toggle_complete" in request.POST:
            self.object.is_completed = not self.object.is_completed
            self.object.save()
            return render(
                request, "tracker/partials/tasks/task_item.html", {"task": self.object}
            )
        form = self.get_form()
        if form.is_valid():
            form.save()
            return render(
                request, "tracker/partials/tasks/task_item.html", {"task": self.object}
            )

        return render(
            request,
            "tracker/partials/tasks/update_task.html",
            {"task": self.object, "form": form},
        )


class TaskDeleteView(DeleteView):
    model = Task

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = HttpResponse()
        # Return an HTMX response to trigger the task list refresh
        response["HX-Trigger"] = "refreshData"
        return response
