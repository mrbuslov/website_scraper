# Generated by Django 3.2.10 on 2022-06-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0003_auto_20220625_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrap',
            name='searching_device',
            field=models.PositiveIntegerField(default=1, verbose_name='Девайс для поиска'),
        ),
        migrations.AlterField(
            model_name='scrap',
            name='slug',
            field=models.SlugField(default='5401b2658de14617ae78089617f2138a', max_length=150, unique=True, verbose_name='Ссылка'),
        ),
    ]
