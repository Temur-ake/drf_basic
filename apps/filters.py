import decimal
from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from django_filters import (BooleanFilter, CharFilter, ChoiceFilter, FilterSet,
                            NumberFilter, RangeFilter)

from django_filters import rest_framework as filters

from .models import Favorite
from apps.models import Category, Product, User


class ProductFilter(FilterSet):
    search = CharFilter(method='search_filter')
    has_image = BooleanFilter(method='has_image_filter')
    owner_type = ChoiceFilter(method='owner_filter', choices=User.Type.choices)
    days = NumberFilter(method='days_filter')
    category = NumberFilter(method='category_')
    price_range = RangeFilter(field_name='price')

    class Meta:
        model = Product
        fields = ['is_premium']

    def days_filter(self, queryset, name, value):
        return queryset.filter(created_at__gte=timezone.now() - timedelta(days=int(value)))

    def has_image_filter(self, queryset, name, value):
        if value:
            return queryset.annotate(image_count=Count('images')).filter(image_count__gt=0)
        return queryset

    def owner_filter(self, queryset, name, value):
        return queryset.filter(owner__type=value)

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    def category_(self, queryset, name, value):
        return queryset.filter(category__id=value)


# filters.py


class FavoriteFilter(filters.FilterSet):
    user = filters.NumberFilter(field_name='user', lookup_expr='exact')
    product = filters.NumberFilter(field_name='product', lookup_expr='exact')

    class Meta:
        model = Favorite
        fields = ['user', 'product']

# class ProductFilter(FilterSet):
#     category_name = CharFilter(method='filter_by_category_name')
#     owner_type = ChoiceFilter(field_name='owner', choices=User.CHOICES, required=False)
#     has_photo = BooleanFilter(method='filter_has_photo')
#     is_premium = BooleanFilter(field_name='is_premium')
#     recent_days = NumberFilter(method='filter_by_recent_days')
#     balance_greater_than = BooleanFilter(method='filter_by_balance')
#
#     class Meta:
#         model = Product
#         fields = ['category_name', 'owner', 'has_photo', 'is_premium', 'recent_days', 'balance_greater_than']
#
#     def filter_by_category_name(self, queryset, name, value):
#         return queryset.filter(category__name__icontains=value)
#
#     def filter_has_photo(self, queryset, name, value):  # TODO togrilash kk
#         if value:
#             return queryset.filter(images__isnull=False).distinct()
#         else:
#             return queryset.filter(images__isnull=True).distinct()
#
#     def filter_by_recent_days(self, queryset, name, value):
#         cutoff_date = timezone.now() - timezone.timedelta(days=int(value))
#         return queryset.filter(created_at__gte=cutoff_date)
#
#     def filter_by_balance(self, queryset, name, value):
#         user = self.request.user
#
#         try:
#             user_profile = user.userprofile
#             user_balance = user_profile.balance
#         except UserProfile.DoesNotExist:
#             return queryset.none()
#
#         if value:
#             return queryset.filter(price__gt=user_balance)
#         return queryset
#
#
