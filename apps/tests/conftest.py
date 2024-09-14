import pytest

from apps.models import Category, Product, User
from apps.tests.factories import ProductFactory


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='securepassword')


@pytest.fixture
def category():
    return Category.objects.create(name='Zo\'r Categoriya')


@pytest.fixture
def product(user, category):
    return ProductFactory.create_batch(10)
