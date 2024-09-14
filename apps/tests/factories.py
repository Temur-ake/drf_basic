from datetime import UTC, tzinfo
from random import choice, randint

import factory
from django.db.models import CASCADE
from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from apps.models import Category, Product, ProductImage, User


class CategoryFactory(DjangoModelFactory):
    name = Faker('company')

    class Meta:
        model = Category

    @factory.lazy_attribute
    def parent(self):
        return choice(Category.objects.all())


class UserFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    username = Faker('user_name')
    email = Faker('email')
    last_login = Faker('date_time', tzinfo=UTC)
    date_joined = Faker('date_time', tzinfo=UTC)
    password = factory.django.Password('1')

    class Meta:
        model = User


class ProductFactory(DjangoModelFactory):
    name = Faker('name')
    is_premium = Faker('boolean')
    description = Faker('text')
    category = SubFactory('apps.tests.factories.CategoryFactory')
    owner = SubFactory('apps.tests.factories.UserFactory')
    created_at = Faker('date_time', tzinfo=UTC)

    class Meta:
        model = Product

    @factory.lazy_attribute
    def price(self):
        return randint(10, 100) * 100


class ProductImageFactory(DjangoModelFactory):
    image = Faker('file_name', category='image', extension='png')
    product = SubFactory('apps.tests.factories.ProductFactory')

    class Meta:
        model = ProductImage
