from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1 import views
from api.v1.views import (APIGetToken, APISignup, UsersViewSet)


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename="comments"
)
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename="reviews"
)
v1_router.register(
    "titles",
    views.TitleViewSet,
    basename="titles"
)
v1_router.register(
    "genres",
    views.GenreViewSet,
    basename='genres'
)
v1_router.register(
    "categories",
    views.CategoriesViewSet,
    basename='сategories'
)
v1_router.register(
    "users",
    UsersViewSet,
    basename='users'
)


urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/token/', APIGetToken.as_view(), name='get_token'),
    path('auth/signup/', APISignup.as_view(), name='signup'),
]
