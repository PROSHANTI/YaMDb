from django.utils import timezone

from django.db import models
from django.core.validators import MaxValueValidator


def get_current_year():
    return timezone.now().year


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

