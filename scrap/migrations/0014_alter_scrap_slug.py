# Generated by Django 3.2.10 on 2022-07-21 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0013_alter_scrap_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrap',
            name='slug',
            field=models.SlugField(default='4bb22de7afa440ec923d6b204fd04fa5', max_length=150, unique=True, verbose_name='Ссылка'),
        ),
    ]
