import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN
from product.models import Product
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# получение списка товаров
@pytest.mark.django_db
def test_get_productlist(unauthorized_client):
    url = reverse("products-list")
    resp = unauthorized_client.get(url)
    assert resp.status_code == HTTP_200_OK


# создание товара авторизованным пользователем
@pytest.mark.django_db
def test_create_product_user(api_client):
    url = reverse("products-list")
    resp = api_client.post(url, {
        'name': 'Шкаф',
        'description': 'Белый',
        'price': '10000',
    }
    )
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Product.objects.count() == 0


# создание товара админом
@pytest.mark.django_db
def test_create_product_admin(admin_client):
    url = reverse("products-list")
    resp = admin_client.post(url, {
        'name': 'Шкаф',
        'description': 'Белый',
        'price': '10000',
    }
    )
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert Product.objects.count() == 1
    assert resp_json['name'] == 'Шкаф'
    return resp_json


# обновление товара авторизованным пользователем
@pytest.mark.django_db
def test_update_user(api_client, admin_client):
    resp_json = test_create_product_admin(admin_client)
    url = reverse("products-detail", args=[resp_json["id"]])
    resp = api_client.patch(url, {
        'name': 'Диван',
        'description': 'Новый',
        'price': '15000',
    })
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert resp_json["name"] == 'Шкаф'


# обновление товара администратором
@pytest.mark.django_db
def test_update_admin(admin_client):
    resp_json = test_create_product_admin(admin_client)
    url = reverse("products-detail", args=[resp_json["id"]])
    resp = admin_client.patch(url, {
        'name': 'Диван',
        'description': 'Новый',
        'price': '15000',
    })
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json["name"] == 'Диван'


