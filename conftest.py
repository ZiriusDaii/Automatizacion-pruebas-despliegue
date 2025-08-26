import pytest
import os
import django

# Configure Django settings for testing BEFORE importing Django components
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winespa.settings')
django.setup()

from django.conf import settings
from django.test import RequestFactory
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """
    Fixture that provides an API client for testing REST endpoints
    """
    return APIClient()


@pytest.fixture
def request_factory():
    """
    Fixture that provides a request factory for testing views
    """
    return RequestFactory()


@pytest.fixture
def db_access_without_rollback_and_truncate(db_access_without_rollback):
    """
    Fixture that provides database access without rollback and truncate
    """
    pass


# Configure pytest to use Django's test database
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enable database access for all tests
    """
    pass


# Add custom markers
def pytest_configure(config):
    """
    Configure pytest with custom markers
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
