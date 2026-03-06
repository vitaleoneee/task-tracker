from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)

from tasktracker.apps.tracker.models import Task, Project


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tracker/partials/tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(
            project_id=self.kwargs["pk"], project__owner=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tracker/partials/tasks/task_item.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "tracker/partials/tasks/task_create.html"
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
        context["project"] = get_object_or_404(Project, pk=self.kwargs["pk"])
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "tracker/partials/tasks/task_update.html"
    fields = ["title", "due_date", "priority"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "toggle_complete" in request.POST:
            self.object.is_completed = not self.object.is_completed
            self.object.save()
        else:
            form = self.get_form()
            if form.is_valid():
                form.save()
            else:
                return render(
                    request,
                    "tracker/partials/tasks/task_update.html",
                    {"task": self.object, "form": form},
                )

        return render(
            request, "tracker/partials/tasks/task_item.html", {"task": self.object}
        )


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = "/"  # not used but Django requires it

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = HttpResponse()
        # Return an HTMX response to trigger the task list refresh
        response["HX-Trigger"] = "refreshData"
        return response
