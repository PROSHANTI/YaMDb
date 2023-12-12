from rest_framework.serializers import IntegerField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from yamdb.models import Category, Genre, Title


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
