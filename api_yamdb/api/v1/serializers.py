from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer


from reviews.models import Category, Comment, Genre, Review, Title, User


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(ModelSerializer):
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
    rating = serializers.IntegerField(read_only=True, default=None)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields

    def get_rating(obj):
        return obj.rating


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

    def to_representation(self, instance):
        serializer = TitleGetSerializer(instance)
        return serializer.data


class GetTokenSerializer(ModelSerializer):
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


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        exclude = ('title', )

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        title = validated_data.get('title')
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                'Разрешен один отзыв от пользователя'
            )
        validated_data['author'] = author
        return super().create(validated_data)
