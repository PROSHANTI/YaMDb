from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from reviews.models import Category, Genre, Title, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        exclude = ("id",)


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        exclude = ("id",)


class TitleSerializer(ModelSerializer):

    class Meta:
        model = Title
        fields = "__all__"


class TitleGetSerializer(TitleSerializer):

    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields


class TitleWriteSerializer(TitleSerializer):

    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="slug",
        many=True,
    )


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')
