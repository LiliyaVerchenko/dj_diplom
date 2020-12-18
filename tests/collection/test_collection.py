import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED
from collection.models import Collection


# просмотр коллекций
@pytest.mark.django_db
def test_get_collections(unauthorized_client):
    url = reverse('collections-list')
    resp = unauthorized_client.get(url)
    assert resp.status_code == HTTP_200_OK


# создание коллекций товаров админом
@pytest.mark.django_db
def test_create_collection_admin(admin_client, product_factory):
    url = reverse('collections-list')
    products = product_factory(_quantity=5)
    resp = admin_client.post(url, {
        "title": "Подборка2",
        "text": "На любой вкус",
        "collections": [{
            "product_id": products[1].id
        },
        {
            "product_id": products[2].id
        }
        ]}, format='json')
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert Collection.objects.count() == 1
    return resp_json


# создание коллекций товаров пользователем
@pytest.mark.django_db
def test_create_collection_user(api_client, product_factory):
    url = reverse('collections-list')
    products = product_factory(_quantity=5)
    resp = api_client.post(url, {
        "title": "Подборка2",
        "text": "На любой вкус",
        "collections": [{
            "product_id": products[1].id
        },
        {
            "product_id": products[2].id
        }
        ]}, format='json')
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Collection.objects.count() == 0