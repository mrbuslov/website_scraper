# Generated by Django 3.2.10 on 2022-06-27 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0006_alter_scrap_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scrap',
            options={'ordering': ['published'], 'verbose_name': 'Scraping', 'verbose_name_plural': 'Scrapings'},
        ),
        migrations.AlterField(
            model_name='scrap',
            name='slug',
            field=models.SlugField(default='4f63ef9d7343497eaf2d2451b6a879f6', max_length=150, unique=True, verbose_name='Ссылка'),
        ),
    ]
