from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import (DateTimeField)
from rest_framework.serializers import ModelSerializer

# from apps.document import ProductDocument
from apps.models import Category, Favorite, Product, ProductImage, User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'balance', 'email'


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = 'id', 'image'


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ()

    def to_representation(self, instance: Product):
        repr = super().to_representation(instance)
        repr['user'] = UserModelSerializer(instance.owner).data
        repr['images'] = ProductImageModelSerializer(instance.images, many=True, context=self.context).data
        return repr


class ProductDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ()

    def to_representation(self, instance: Product):
        repr = super().to_representation(instance)
        repr['category'] = CategoryModelSerializer(instance.category).data
        return repr


class FavoriteSerializer(ModelSerializer):
    user = UserModelSerializer
    product = ProductListModelSerializer()
    created_at = DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Favorite
        fields = ['user', 'product', 'created_at']


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255,
        help_text='kozimovt0@gmail.com'
    )

    def validate_email(self, value):
        if not value:
            raise ValidationError('Email is required')
        return value


# class ProductDocumentSerializer(serializers.Serializer):
#     class Meta:
#         model = ProductDocument
#         exclude = ()


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255,
        help_text='kozimovt0@gmail.com'
    )
    code = serializers.IntegerField(
        help_text='Enter the 4-digit code sent to your email'
    )

    def validate_email(self, value):
        if not value:
            raise ValidationError('Email is required')
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        cache_code = cache.get(email)  # Use email to get the code from cache
        if code != cache_code:
            raise ValidationError('The code is incorrect or has expired!')
        return attrs
