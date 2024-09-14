from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline, register
from django.contrib.auth.admin import UserAdmin

from apps.models import Category, Product, ProductImage, User


# Register your models here.
@register(Category)
class CategoryModelAdmin(ModelAdmin):
    list_display = 'name',


class ProductStackedInline(StackedInline):
    model = ProductImage
    extra = 1
    min_num = 1


@register(Product)
class ProductModelAdmin(ModelAdmin):
    list_display = 'name',
    inlines = [ProductStackedInline]


@register(ProductImage)
class ProductImageModelAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'balance']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "balance"),
            },
        ),
    )
