import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from tests.product.test_product import test_create_product_admin
from review.models import Review


# просмотр списка отзывов
@pytest.mark.django_db
def test_get_reviews(unauthorized_client):
    url = reverse('reviews-list')
    resp = unauthorized_client.get(url)
    assert resp.status_code == HTTP_200_OK


# создание отзыва неавторизованным пользователем
@pytest.mark.django_db
def test_create_review_unauthorized(unauthorized_client, admin_client):
    url = reverse('reviews-list')
    new_product = test_create_product_admin(admin_client)
    resp = unauthorized_client.post(url, {
        'product_id': new_product["id"],
        'rating': '4',
        'text': 'Норм',
    }
    )
    assert resp.status_code == HTTP_401_UNAUTHORIZED


# создание отзыва авторизованным пользователем
@pytest.mark.django_db
def test_create_review_user(api_client, admin_client):
    url = reverse('reviews-list')
    new_product = test_create_product_admin(admin_client)
    resp = api_client.post(url, {
        'product_id': new_product['id'],
        'rating': '4',
        'text': 'Норм',
    }
    )
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert Review.objects.count() == 1
    assert resp_json['product_id'] == new_product['id']
    resp = api_client.post(url, {
        'product_id': new_product['id'],
        'rating': '5',
        'text': 'Норм',
    }
    )
    assert Review.objects.filter(product_id=resp_json['product_id']).filter(
        author_id=resp_json['author_id']['id']).count() == 1


# обновление и удаление своего отзыва
@pytest.mark.django_db
def test_update_or_delete_own_review(api_client, admin_client):
    url = reverse('reviews-list')
    new_product = test_create_product_admin(admin_client)
    resp = api_client.post(url, {
        'product_id': new_product['id'],
        'rating': '4',
        'text': 'Хорошо',
    }
    )
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert Review.objects.count() == 1
    assert resp_json['product_id'] == new_product['id']

    url = reverse("reviews-detail", args=[resp_json['author_id']["id"]])
    resp = api_client.patch(url, {
        'product_id': new_product['id'],
        'rating': '5',
        'text': 'Отлично',
    }
    )
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json["rating"] == 5
    assert resp_json["text"] == 'Отлично'

    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0


# обновление и удаление чужого отзыва
@pytest.mark.django_db
def test_update_or_delete_else_review(api_client, review_factory):
    review = review_factory()
    assert Review.objects.count() == 1
    url = reverse("reviews-detail", args=[review.id])
    resp = api_client.patch(url, {
        'text': 'Цена-качество',
        'rating': '4',
    })
    assert resp.status_code == HTTP_403_FORBIDDEN
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Review.objects.count() == 1

