from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from api.v1 import permissions
from api.v1 import serializers
from api.v1.filters import TitleFilter
from api.v1.mixins import GenreCategoryMixin
from yamdb.models import Title, Genre, Category


class TitleViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.TitleGetSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.TitleGetSerializer
        return serializers.TitleWriteSerializer


class GenreViewSet(GenreCategoryMixin):

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (SearchFilter,)


class CategoriesViewSet(GenreCategoryMixin):

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (SearchFilter,)

