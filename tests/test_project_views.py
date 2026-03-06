"""Tests for project views"""

import json
import pytest
from django.urls import reverse
from tasktracker.apps.tracker.models import Project
from tests.factories import UserFactory, ProjectFactory


@pytest.mark.django_db
class TestProjectViews:
    """Tests for all project views"""

    def test_list_requires_login(self, client):
        """Require login for project list"""
        url = reverse("tracker:project_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_list_shows_user_projects(self, authenticated_client, user):
        """Show only user projects"""
        user_project = ProjectFactory(owner=user, name="Mine")
        other_project = ProjectFactory(owner=UserFactory(), name="Other")

        url = reverse("tracker:project_list")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert user_project in response.context["projects"]
        assert other_project not in response.context["projects"]

    def test_list_empty(self, authenticated_client):
        """Handle empty project list"""
        url = reverse("tracker:project_list")
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_list_multiple(self, authenticated_client, user):
        """Show multiple projects"""
        ProjectFactory(owner=user)
        ProjectFactory(owner=user)
        url = reverse("tracker:project_list")
        response = authenticated_client.get(url)
        assert response.context["projects"].count() == 2

    def test_detail_requires_login(self, client, project):
        """Require login for project detail"""
        url = reverse("tracker:project_detail", kwargs={"pk": project.pk})
        response = client.get(url)
        assert response.status_code == 302

    def test_detail_view(self, authenticated_client, user):
        """Display project detail"""
        project = ProjectFactory(owner=user, name="Test")
        url = reverse("tracker:project_detail", kwargs={"pk": project.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.context["project"] == project

    def test_detail_forbidden(self, authenticated_client):
        """Forbid access to other user project"""
        project = ProjectFactory(owner=UserFactory())
        url = reverse("tracker:project_detail", kwargs={"pk": project.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 404

    def test_create_requires_login(self, client):
        """Require login for project creation"""
        url = reverse("tracker:project_add")
        response = client.post(url, {"name": "new"})
        assert response.status_code == 302

    def test_create_success(self, authenticated_client, user):
        """Create new project"""
        url = reverse("tracker:project_add")
        response = authenticated_client.post(url, {"name": "new"})
        assert response.status_code == 200
        project = Project.objects.get(name="new")
        assert project.owner == user

    def test_create_htmx_response(self, authenticated_client):
        """Return HTMX response"""
        url = reverse("tracker:project_add")
        response = authenticated_client.post(url, {"name": "new"})
        assert "HX-Trigger" in response
        trigger = json.loads(response["HX-Trigger"])
        assert trigger["closeModal"] is True

    def test_update_requires_login(self, client, project):
        """Require login for project update"""
        url = reverse("tracker:project_update", kwargs={"pk": project.pk})
        response = client.post(url, {"name": "updated"})
        assert response.status_code == 302

    def test_update_success(self, authenticated_client, user):
        """Update project"""
        project = ProjectFactory(owner=user, name="old")
        url = reverse("tracker:project_update", kwargs={"pk": project.pk})
        response = authenticated_client.post(url, {"name": "new"})
        assert response.status_code == 200
        project.refresh_from_db()
        assert project.name == "new"

    def test_delete_success(self, authenticated_client, user):
        """Delete project"""
        project = ProjectFactory(owner=user)
        url = reverse("tracker:project_delete", kwargs={"pk": project.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == 200
        assert not Project.objects.filter(pk=project.pk).exists()

    def test_delete_requires_login(self, client, project):
        """Require login for project deletion"""
        url = reverse("tracker:project_delete", kwargs={"pk": project.pk})
        response = client.post(url)
        assert response.status_code == 302
