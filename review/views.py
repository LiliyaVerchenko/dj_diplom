from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from review.models import Review
from review.serializers import ReviewSerializer
from rest_framework import permissions
from review.filters import ReviewFilter


class ReviewPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            if request.method == 'POST':
                return True
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                try:
                    review = Review.objects.get(id=request.parser_context['kwargs']['pk'])
                except:
                    raise NotFound({'Error': 'Отзыв не найден'})
                if review.author_id.username == request.user.username:
                    return True
        return []

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]


class ReviewViewSet(ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermissions,)
    filterset_class = ReviewFilter
