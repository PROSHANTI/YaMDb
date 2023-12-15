from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1 import permissions
from api.v1 import serializers
from api.v1.filters import TitleFilter
from api.v1.mixins import GenreCategoryMixin
from api.v1.permissions import IsAdmin
from api.v1.serializers import (GetTokenSerializer,
                                NotAdminSerializer,
                                ReviewSerializer,
                                SignUpSerializer,
                                UsersSerializer,
                                )

from reviews.models import Category, Genre, Review, Title, User


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):

    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена. Пример тела запроса:
    {
        "username": "string",
        "confirmation_code": "string"
    }
    """

    @staticmethod
    def post(request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):

    """
    Получить код подтверждения на переданный email. Права доступа: Доступно без
    токена. Использовать имя 'me' в качестве username запрещено. Поля email и
    username должны быть уникальными. Пример тела запроса:
    {
        "email": "string",
        "username": "string"
    }
    """

    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        if request.data.get("username") and User.objects.filter(
            username=request.data.get("username")
        ).exists():
            user = User.objects.get(username=request.data.get("username"))

            if user.email != request.data.get("email"):
                return Response(
                    {
                        "detail":"Пользователь с такой почтой уже существует."
                    },
                    status=status.HTTP_400_BAD_REQUEST)

            email_body = (
                f'Доброе время суток, {user.username}.'
                f'\nКод подтверждения для доступа к API: '
                f'{user.confirmation_code}'
            )
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Код подтверждения для доступа к API!'
            }
            self.send_email(data)
            return Response("Код подтверждения повторно отправлен",
                            status=status.HTTP_200_OK
                            )

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Доброе время суток, {user.username}.'
            f'\nКод подтверждения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения для доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Получить список всех объектов. Права доступа: Доступно без токена."""

    queryset = Title.objects.all()
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.TitleGetSerializer
        return serializers.TitleWriteSerializer


class GenreViewSet(GenreCategoryMixin):
    """Получить список всех жанров. Права доступа: Доступно без токена."""

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (SearchFilter,)


class CategoriesViewSet(GenreCategoryMixin):
    """Получить список всех категорий. Права доступа: Доступно без токена."""

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (SearchFilter,)


class ReviewViewSet(viewsets.ModelViewSet):
    """Получить список всех отзывов. Права доступа: Доступно без токена."""

    serializer_class = ReviewSerializer
    permission_classes = (permissions.AuthorModerAdmin,)

    def object_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.object_title().reviews.all()

    def perform_create(self, serializer):
        if Review.objects.filter(author=self.request.user,
                                 title=self.object_title()):
            raise ParseError('Разрешен один отзыв')

        sum_score = 0
        query = Review.objects.filter(
            title=self.object_title().pk
        )

        for i in query:
            sum_score += i.score

        try:
            avg_score = sum_score / len(query)
            Title.objects.filter(
                pk=self.object_title().pk
            ).update(rating=avg_score)
        except ZeroDivisionError:
            avg_score = sum_score

        serializer.save(
            author=self.request.user,
            title=self.object_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Получить комментарий. Права доступа: Доступно без токена."""

    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.AuthorModerAdmin,)

    def object_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.object_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.object_review())
