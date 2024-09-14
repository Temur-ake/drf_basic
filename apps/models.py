from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import (CASCADE, BooleanField, CharField, DateTimeField,
                              EmailField, ForeignKey, ImageField, IntegerField,
                              Model, TextChoices, TextField, SlugField)
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


class SlugBaseModel(models.Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '1'
        super().save(force_insert, force_update, using, update_fields)


class Category(SlugBaseModel):
    pass


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
        MANAGER = 'manager', 'Manager'
        MODERATOR = 'moderator', 'Moderator'

    balance = IntegerField(db_default=0)
    email = EmailField()
    type = CharField(max_length=25, choices=Type.choices, db_default=Type.USER)


class Product(Model):
    name = CharField(max_length=255)
    price = IntegerField()
    is_premium = BooleanField(db_default=False)
    description = TextField(null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    owner = ForeignKey('apps.User', CASCADE, related_name='products')
    created_at = DateTimeField(auto_now_add=True)


class ProductImage(Model):
    image = ImageField(upload_to='products/')
    product = ForeignKey('apps.Product', CASCADE, related_name='images')


class Favorite(Model):
    user = ForeignKey(User, CASCADE, related_name='favorites')
    product = ForeignKey(Product, CASCADE, related_name='favorited_by')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']


class ProductHistory(Model):
    name = CharField(max_length=255)
    price = IntegerField()
    is_premium = BooleanField(db_default=False)
    description = TextField(null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE)
    owner = ForeignKey('apps.User', CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    deleted_at = DateTimeField(auto_now_add=True)
