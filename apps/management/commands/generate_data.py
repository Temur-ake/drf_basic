from random import choice, randint

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker

from apps.models import Category, Favorite, Product, User


class Command(BaseCommand):
    help = 'Generating fake data'
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-c', '--category', type=int)
        parser.add_argument('-u', '--user', type=int)
        parser.add_argument('-p', '--product', type=int)

    def _category(self, n: int):
        for i in range(n):
            Category.objects.create(name=self.fake.company())
        self.stdout.write(self.style.SUCCESS(f'Successfully added {n} category'))

    def _user(self, n: int):
        users_list = []
        for i in range(n):
            users_list.append(User(
                first_name=self.fake.name(),
                last_name=self.fake.name(),
                username=self.fake.user_name(),
                type=choice(User.Type.choices)[0],
                balance=randint(100, 5000) * 1000,
                password=make_password(self.fake.password(5))
            ))
        User.objects.bulk_create(users_list)
        self.stdout.write(self.style.SUCCESS(f'Successfully added {n} users'))

    def _product(self, n: int):
        product_list = []
        for i in range(n):
            product_list.append(Product(
                name=self.fake.name(),
                price=randint(10, 150) * 1000,
                is_premium=bool(randint(1, 100) & 1),
                description=self.fake.text(),
                category_id=choice(Category.objects.values_list('id', flat=True)),
                owner_id=choice(User.objects.values_list('id', flat=True)),
                created_at=self.fake.date_time()
            ))

        Product.objects.bulk_create(product_list)
        self.stdout.write(self.style.SUCCESS(f'Successfully added {n} products'))

    def _favorites(self, n: int):
        users = User.objects.all()
        products = Product.objects.all()
        favorites_list = []

        for _ in range(n):
            user = choice(users)
            product = choice(products)
            favorites_list.append(Favorite(user=user, product=product))

        Favorite.objects.bulk_create(favorites_list)
        self.stdout.write(self.style.SUCCESS(f'Successfully added {n} favorites'))

    def handle(self, *args, **options):
        actions = {'user': 'user', 'category': 'category', 'product': 'product'}

        for action in actions:
            if options.get(action):
                getattr(self, f'_{actions[action]}')(options[action])

        self.stdout.write(self.style.SUCCESS(f'Successfully added data'))
