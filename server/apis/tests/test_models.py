import pytest

from .factories import UserFactory
from apis.models import User


pytestmark = pytest.mark.django_db


def test_user_factory(user_factory):
    assert user_factory is UserFactory


def test_user():
    User.objects.create_user(username='admin', email='admin@gmail.com', password='12345678')
    user = User.objects.get(username="admin")
    assert user.is_active