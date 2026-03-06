"""
Factories for generating test data
"""

import factory
from django.contrib.auth.models import User
from django.utils import timezone

from tasktracker.apps.tracker.models import Project, Task


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating test users"""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")


class ProjectFactory(factory.django.DjangoModelFactory):
    """Factory for creating test projects"""

    class Meta:
        model = Project

    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Project {n}")
    created_at = factory.LazyFunction(timezone.now)


class TaskFactory(factory.django.DjangoModelFactory):
    """Factory for creating test tasks"""

    class Meta:
        model = Task

    project = factory.SubFactory(ProjectFactory)
    title = factory.Sequence(lambda n: f"Task {n}")
    is_completed = False
    priority = Task.Priority.MEDIUM
    due_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=7))
    created_at = factory.LazyFunction(timezone.now)
