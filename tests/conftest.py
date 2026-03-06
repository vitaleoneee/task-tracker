"""Fixtures for tests"""

import pytest
from tests.factories import ProjectFactory, TaskFactory, UserFactory


@pytest.fixture
def user(db):
    """Create test user"""
    return UserFactory()


@pytest.fixture
def authenticated_client(client, user):
    """Create authenticated test client"""
    client.force_login(user)
    return client


@pytest.fixture
def project(db, user):
    """Create test project"""
    return ProjectFactory(owner=user)


@pytest.fixture
def task(db, project):
    """Create test task"""
    return TaskFactory(project=project)
