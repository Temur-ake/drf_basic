from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from apps.views import (CategoryDetailApiview, CategoryListAPIView,
                        FavoriteListView, ProductDetailView,
                        ProductListAPIView, SendCodeAPIView, UserAPIView,
                        VerifyCodeAPIView)

# router = DefaultRouter()
# router.register('products', ProductDocumentViewSet, 'products')
urlpatterns = [
    # path('', include(router.urls)),

    path('postgres-products', ProductListAPIView.as_view(), name='products'),
    path('categories', CategoryListAPIView.as_view(), name='categories'),
    path('categories/<int:pk>', CategoryDetailApiview.as_view(), name='category-detail'),
    path('products/<int:pk>', ProductDetailView.as_view()),
    # path('products/<int:pk>', ProductCreateAPIView.as_view()),
    path('user', UserAPIView.as_view()),
    path('favorites/', FavoriteListView.as_view()),
    path('auth/send-code/', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify/', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),

]
