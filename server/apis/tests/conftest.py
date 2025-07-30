import pytest

from rest_framework.test import APIClient
from pytest_factoryboy import register

from .factories import UserFactory

register(UserFactory)

@pytest.fixture
def api_client():
    return APIClient()