from rest_framework import mixins, viewsets

from api.v1.permissions import IsAdminOrReadOnly


class GenreCategoryMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name",)
    lookup_field = "slug"
