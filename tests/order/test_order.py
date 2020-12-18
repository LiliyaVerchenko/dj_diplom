import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from order.models import Order
from tests.product.test_product import test_create_product_admin
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_order_unauthorized(unauthorized_client, api_client, admin_client):
    url = reverse('orders-list')
    new_product = test_create_product_admin(admin_client)

    # создание заказа неавторизованным пользователем
    resp = unauthorized_client.post(url, {
        "orders_in": [
            {
                "product_id": new_product['id'],
                "quantity": 7,
            }
        ]
    })
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    assert Order.objects.count() == 0


# создание заказа авторизованным пользователем
@pytest.mark.django_db
def test_create_order_user(api_client, admin_client):
    url = reverse('orders-list')
    # new_product = product_factory()
    new_product = test_create_product_admin(admin_client)
    resp = api_client.post(url, {
        "orders_in": [
            {
                "product_id": new_product['id'],
                "quantity": 2,
            }
        ]
    }, format='json')
    assert resp.status_code == HTTP_201_CREATED
    assert Order.objects.count() == 1


# получение списка всех заказов админом
@pytest.mark.django_db
def test_get_admin_orderlist(admin_client, order_factory):
    url = reverse('orders-list')
    order_factory(client=User.objects.get(username='admin'), _quantity=5)
    resp = admin_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 5


# получение списка своиз заказов авторизованными пользователями
@pytest.mark.django_db
def test_get_user_own_orderlist(api_client, order_factory):
    url = reverse('orders-list')
    order_factory(client=User.objects.get(username='user123'), _quantity=5)
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 5


# изменение статуса заказа авторизованным пользователем
@pytest.mark.django_db
def test_update_status_order_user(api_client, admin_client, order_factory):
    new_order = order_factory(client=User.objects.get(username='user123'))
    url = reverse("orders-detail", args=[new_order.id])
    resp = api_client.patch(url, {
        "status": "IN_PROGRESS"
    }
    )
    assert resp.status_code == HTTP_403_FORBIDDEN


    # изменение статуса заказа админом
    resp = admin_client.patch(url, {
            "status": "IN_PROGRESS"
    }
    )
    assert resp.status_code == HTTP_200_OK
