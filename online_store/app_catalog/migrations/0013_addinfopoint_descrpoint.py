# Generated by Django 2.2 on 2023-02-15 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0012_auto_20230214_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescrPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='содержание')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descr_points', to='app_catalog.Product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'пункт описания',
                'verbose_name_plural': 'пункты описания',
            },
        ),
        migrations.CreateModel(
            name='AddInfoPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('characteristic', models.CharField(max_length=255, verbose_name='характеристика')),
                ('value', models.CharField(max_length=255, verbose_name='значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_info_points', to='app_catalog.Product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'пункт доп. информации',
                'verbose_name_plural': 'пункты доп. информации',
            },
        ),
    ]