# Generated by Django 2.2 on 2022-10-18 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0003_auto_20221018_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='описание'),
        ),
    ]
