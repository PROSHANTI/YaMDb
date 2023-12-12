from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1 import views


router = DefaultRouter()

router.register("titles", views.TitleViewSet, basename="titles")
router.register("genres", views.GenreViewSet)
router.register("categories", views.CategoriesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
