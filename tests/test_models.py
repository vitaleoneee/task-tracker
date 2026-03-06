"""Tests for tracker models"""

import pytest
from tests.factories import ProjectFactory, TaskFactory


@pytest.mark.django_db
class TestModels:
    """Tests for Project and Task models"""

    def test_project_str(self):
        """Test project string representation"""
        project = ProjectFactory(name="Test")
        assert str(project) == "Test"

    def test_task_str(self):
        """Test task string representation"""
        task = TaskFactory(title="My Task")
        assert str(task) == "My Task"
