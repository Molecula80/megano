# Generated by Django 2.2 on 2023-02-14 21:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0010_auto_20221227_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]
