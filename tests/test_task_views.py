import pytest
from django.urls import reverse
from django.utils import timezone
from tasktracker.apps.tracker.models import Task
from tests.factories import UserFactory, ProjectFactory, TaskFactory


@pytest.mark.django_db
class TestTaskViews:
    """Tests for all task views"""

    def test_list_shows_project_tasks(self, authenticated_client, user):
        """Show only project tasks"""
        project = ProjectFactory(owner=user)
        other_project = ProjectFactory(owner=UserFactory())

        task1 = TaskFactory(project=project, title="first")
        task2 = TaskFactory(project=other_project, title="second")

        url = reverse("tracker:task_list", kwargs={"pk": project.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert task1 in response.context["tasks"]
        assert task2 not in response.context["tasks"]

    def test_list_empty(self, authenticated_client, user):
        """Handle empty task list"""
        project = ProjectFactory(owner=user)
        url = reverse("tracker:task_list", kwargs={"pk": project.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_list_multiple(self, authenticated_client, user):
        """Show multiple tasks"""
        project = ProjectFactory(owner=user)
        TaskFactory(project=project)
        TaskFactory(project=project)
        url = reverse("tracker:task_list", kwargs={"pk": project.pk})
        response = authenticated_client.get(url)
        assert response.context["tasks"].count() == 2

    def test_detail_view(self, authenticated_client, task):
        """Display task detail"""
        url = reverse("tracker:task_detail", kwargs={"pk": task.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_detail_not_found(self, authenticated_client):
        """Handle missing task"""
        url = reverse("tracker:task_detail", kwargs={"pk": 100})
        response = authenticated_client.get(url)
        assert response.status_code == 404

    def test_create_success(self, authenticated_client, user):
        """Create new task"""
        project = ProjectFactory(owner=user)
        url = reverse("tracker:task_add", kwargs={"pk": project.pk})
        data = {"title": "New", "priority": Task.Priority.HIGH}
        response = authenticated_client.post(url, data)
        assert response.status_code == 200
        task = Task.objects.get(title="New")
        assert task.project == project

    def test_create_with_due_date(self, authenticated_client, user):
        """Create task with due date"""
        project = ProjectFactory(owner=user)
        url = reverse("tracker:task_add", kwargs={"pk": project.pk})
        due = timezone.now() + timezone.timedelta(days=5)
        data = {"title": "Task", "priority": Task.Priority.MEDIUM, "due_date": due}
        response = authenticated_client.post(url, data)
        assert response.status_code == 200
        task = Task.objects.get(title="Task")
        assert task.due_date is not None

    def test_create_htmx_response(self, authenticated_client, user):
        """Return HTMX response on create"""
        project = ProjectFactory(owner=user)
        url = reverse("tracker:task_add", kwargs={"pk": project.pk})
        data = {"title": "New", "priority": Task.Priority.LOW}
        response = authenticated_client.post(url, data)
        assert "HX-Trigger" in response
        assert response["HX-Trigger"] == "refreshData"

    def test_update_success(self, authenticated_client, user):
        """Update task"""
        project = ProjectFactory(owner=user)
        task = TaskFactory(project=project, title="old")
        url = reverse("tracker:task_update", kwargs={"pk": task.pk})
        data = {"title": "new", "priority": Task.Priority.HIGH}
        response = authenticated_client.post(url, data)
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.title == "new"

    def test_update_toggle_complete(self, authenticated_client, user):
        """Toggle task completion"""
        project = ProjectFactory(owner=user)
        task = TaskFactory(project=project, is_completed=False)
        url = reverse("tracker:task_update", kwargs={"pk": task.pk})
        response = authenticated_client.post(url, {"toggle_complete": "true"})
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.is_completed is True

    def test_delete_success(self, authenticated_client, user):
        """Delete task"""
        project = ProjectFactory(owner=user)
        task = TaskFactory(project=project)
        url = reverse("tracker:task_delete", kwargs={"pk": task.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == 200

    def test_delete_htmx_response(self, authenticated_client, user):
        """Return HTMX response on delete"""
        project = ProjectFactory(owner=user)
        task = TaskFactory(project=project)
        url = reverse("tracker:task_delete", kwargs={"pk": task.pk})
        response = authenticated_client.delete(url)
        assert "HX-Trigger" in response
        assert response["HX-Trigger"] == "refreshData"

    def test_delete_not_found(self, authenticated_client):
        """Handle missing task on delete"""
        url = reverse("tracker:task_delete", kwargs={"pk": 111})
        response = authenticated_client.post(url)
        assert response.status_code == 404
