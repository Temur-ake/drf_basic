from random import randint

from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Count
#from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
#from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from apps.document import ProductDocument
from apps.filters import FavoriteFilter, ProductFilter
from apps.models import Category, Favorite, Product, User
from apps.serializers import (CategoryDetailSerializer,
                              CategoryModelSerializer, FavoriteSerializer,
                              ProductDetailModelSerializer,
                              ProductListModelSerializer, SendCodeSerializer,
                              UserModelSerializer, VerifyCodeSerializer)


# Create your views here.
@extend_schema(tags=['category'])
class CategoryListAPIView(ListCreateAPIView):
    serializer_class = CategoryModelSerializer

    def get_queryset(self):
        return Category.objects.annotate(
            products_count=Count('products') + Count('children__products')
        )


@extend_schema(tags=['category'])
class CategoryDetailApiview(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.order_by('name')
    serializer_class = CategoryDetailSerializer


@extend_schema(tags=['product'])
class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.order_by('name')
    serializer_class = ProductListModelSerializer
    filterset_class = ProductFilter


@extend_schema(tags=['product'])
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['product'])
class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['user'])
class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


@extend_schema(tags=['favourite'])
class FavoriteListView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    filterset_class = FavoriteFilter


# class ProductDocumentViewSet(DocumentViewSet):
#     document = ProductDocument
#     serializer_class = ProductDocumentSerializer
#
#     filter_backends = [
#         SearchFilterBackend
#     ]
#     search_fields = ('name', 'description')


@extend_schema(tags=['email'])
class SendCodeAPIView(GenericAPIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = randint(1000, 9999)
        cache.set(email, code, timeout=120)
        print(f"Email: {email}, Code: {code}")
        send_mail(
            'Your Verification Code',
            f'Your verification code is {code}',
            'kozimovt0@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Code sent successfully"}, status=status.HTTP_200_OK)


@extend_schema(tags=['verify'])
class VerifyCodeAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "OK"}, status=status.HTTP_200_OK)
