import pytest
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from apps.models import Category
from apps.tests.factories import CategoryFactory


@pytest.mark.django_db
class TestViews:
    # def test_category(self, client, category):
    #     url = reverse_lazy('categories')
    #     response = client.get(url)
    #     data = response.json()
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(data['results']) == 1
    #     assert data[0]['name'] == category.name

    # def test_category_pagination(self, client):
    #     page_count = 10
    #     CategoryFactory.create_batch(page_count)
    #
    #     url = reverse_lazy('categories')
    #     response = client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     response = response.json()
    #     assert response['count'] == page_count
    #     next_page_url = reverse_lazy('categories') + '?' + urlencode({'page': 2})
    #     assert next_page_url in response['next']
    #
    #     response = client.get(next_page_url)
    #     assert response.status_code == status.HTTP_200_OK
    #     response = response.json()
    #     prev_page_url = reverse_lazy('categories')
    #     assert response['next'] is None
    #     assert str(prev_page_url) in response['previous']

    def test_category_create(self, client):
        url = reverse_lazy('categories')
        data = {
            'name': 'New Category'
        }
        response = client.post(url, data)
        response_data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert response_data['name'] == data['name']
        _category = Category.objects.first()

        assert _category.name == data['name']
        assert Category.objects.count() == 1

    def test_category_update(self, client, category):
        url = reverse_lazy('category-detail', kwargs={'pk': category.id})
        data = {
            'name': 'Updated Category'
        }
        response = client.put(url, data, content_type='application/json')
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data['name'] == data['name']
        category.refresh_from_db()
        assert category.name == response_data['name']

    def test_category_delete(self, client, category):
        category_count = Category.objects.count()
        url = reverse_lazy('category-detail', kwargs={'pk': category.id})
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Category.objects.count() == category_count - 1

    # def test_product(self, client, product):
    #     url = reverse_lazy('products')
    #     response = client.get(url)
    #     data = response.json()
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(data) == 4
    #     assert data[0]['name'] == product.name

    def test_product_filter_has_image(self, client, product):
        query = {
            'has_image': True
        }
        url = reverse_lazy('products')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for i in response['results']:
            assert len(i['images'])

    def test_product_filter_is_premium(self, client, product):
        query = {
            'is_premium': True
        }
        url = reverse_lazy('products')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for i in response['results']:
            assert i['is_premium']

    def test_product_filter_search(self, client, product):
        key = 'produCT'
        query = {
            'search': key
        }
        url = reverse_lazy('products')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for i in response['results']:
            a = i['name'].lower()
            b = i['description'].lower()
            assert key.lower() in a or key.lower() in b

    def test_product_filter_category(self, client, product, category):
        query = {
            'category': category.id
        }
        url = reverse_lazy('products')
        response = client.get(url, query)

        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for i in response['results']:
            assert i['category'] == category.id

    def test_product_filter_price(self, client, product):
        max = 15000
        min = 2000
        query = {
            'price_range_max': 15000,
            'price_range_min': 2000
        }
        url = reverse_lazy('products')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for i in response['results']:
            assert min <= i['price'] <= max
