"""Integration tests"""

import pytest
from django.urls import reverse
from tasktracker.apps.tracker.models import Project, Task
from tests.factories import UserFactory, ProjectFactory


@pytest.mark.django_db
class TestIntegration:
    """Integration tests for workflows"""

    def test_create_and_view_project(self, authenticated_client, user):
        """Create project and view it"""
        create_url = reverse("tracker:project_add")
        response = authenticated_client.post(create_url, {"name": "My"})
        assert response.status_code == 200

        project = Project.objects.get(name="My")
        list_url = reverse("tracker:project_list")
        response = authenticated_client.get(list_url)
        assert project in response.context["projects"]

    def test_task_lifecycle(self, authenticated_client, user):
        """Create task, complete and delete it"""
        project = ProjectFactory(owner=user)

        # Create
        create_url = reverse("tracker:task_add", kwargs={"pk": project.pk})
        response = authenticated_client.post(
            create_url, {"title": "Todo", "priority": Task.Priority.HIGH}
        )
        assert response.status_code == 200

        # Complete
        task = Task.objects.get(title="Todo")
        update_url = reverse("tracker:task_update", kwargs={"pk": task.pk})
        response = authenticated_client.post(update_url, {"toggle_complete": "true"})
        assert response.status_code == 200

        task.refresh_from_db()
        assert task.is_completed is True

        # Delete
        delete_url = reverse("tracker:task_delete", kwargs={"pk": task.pk})
        response = authenticated_client.delete(delete_url)
        assert response.status_code == 200
        assert not Task.objects.filter(pk=task.pk).exists()

    def test_user_isolation(self, client):
        """Users see only own projects"""
        user1 = UserFactory()
        user2 = UserFactory()
        p1 = ProjectFactory(owner=user1, name="User1")
        p2 = ProjectFactory(owner=user2, name="User2")

        client.force_login(user1)
        url1 = reverse("tracker:project_detail", kwargs={"pk": p1.pk})
        response = client.get(url1)
        assert response.status_code == 200

        url2 = reverse("tracker:project_detail", kwargs={"pk": p2.pk})
        response = client.get(url2)
        assert response.status_code == 404

    def test_task_priorities(self, authenticated_client, user):
        """Create tasks with all priorities"""
        project = ProjectFactory(owner=user)
        priorities = [
            Task.Priority.LOW,
            Task.Priority.MEDIUM,
            Task.Priority.HIGH,
            Task.Priority.CRITICAL,
        ]

        for priority in priorities:
            url = reverse("tracker:task_add", kwargs={"pk": project.pk})
            data = {"title": f"Task{priority}", "priority": priority}
            response = authenticated_client.post(url, data)
            assert response.status_code == 200

        tasks = Task.objects.filter(project=project)
        assert tasks.count() == len(priorities)
