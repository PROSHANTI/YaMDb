# Generated by Django 3.2 on 2023-12-14 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20231214_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.FloatField(blank=True, null=True, verbose_name='Рейтинг'),
        ),
    ]
