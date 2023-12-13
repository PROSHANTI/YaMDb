from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.dispatch import receiver
from django.utils import timezone


from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save

from .validators import validate_username


def get_current_year():
    return timezone.now().year


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.confirmation_code = confirmation_code
        instance.save()


class DefaultModel(models.Model):
    """Абстрактная модель."""

    name = models.CharField(
        verbose_name="Название",
        max_length=256,
        db_index=True,
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        max_length=50,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Genre(DefaultModel):

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        default_related_name = "genres"
    

class Category(DefaultModel):

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        default_related_name = "categories"


class Title(models.Model):

    name = models.CharField(
        verbose_name="Название",
        max_length=256,
        db_index=True,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год создания",
        db_index=True,
        validators=[MaxValueValidator(get_current_year)],
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        verbose_name="Жанр",
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre} {self.title}"
