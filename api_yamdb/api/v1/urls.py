from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1 import views


v1_router = DefaultRouter()

v1_router.register("titles", views.TitleViewSet, basename="titles")
v1_router.register("genres", views.GenreViewSet)
v1_router.register("categories", views.CategoriesViewSet)

urlpatterns = [
    path("", include(v1_router.urls)),
]
