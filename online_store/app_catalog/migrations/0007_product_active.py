# Generated by Django 2.2 on 2022-10-30 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0006_addinfopoint_descrpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=False, verbose_name='активно'),
        ),
    ]
