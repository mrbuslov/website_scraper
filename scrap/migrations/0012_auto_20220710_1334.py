# Generated by Django 3.2.10 on 2022-07-10 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0011_alter_scrap_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatedfile',
            name='celery_task_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Celery task id'),
        ),
        migrations.AlterField(
            model_name='scrap',
            name='slug',
            field=models.SlugField(default='612b8cd5eb204c26820b4045b9b86bf2', max_length=150, unique=True, verbose_name='Ссылка'),
        ),
    ]
