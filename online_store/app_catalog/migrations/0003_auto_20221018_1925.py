# Generated by Django 2.2 on 2022-10-18 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0002_auto_20220924_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fabricator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название')),
            ],
            options={
                'verbose_name': 'производитель',
                'verbose_name_plural': 'производители',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='images/categories/', verbose_name='иконка'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название')),
                ('slug', models.SlugField(max_length=255, unique_for_date='added_at')),
                ('description', models.CharField(max_length=1000, verbose_name='описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('num_purchases', models.PositiveIntegerField(default=0, verbose_name='количество покупок')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/products/', verbose_name='иконка')),
                ('sort_index', models.PositiveIntegerField(verbose_name='индекс сортировки')),
                ('in_stock', models.BooleanField(default=False, verbose_name='в наличии')),
                ('free_delivery', models.BooleanField(default=False, verbose_name='с бесплатной доставкой')),
                ('limited_edition', models.BooleanField(default=False, verbose_name='ограниченный тираж')),
                ('added_at', models.DateTimeField(verbose_name='дата публикации')),
                ('categories', models.ManyToManyField(related_name='products', to='app_catalog.Category', verbose_name='категории')),
                ('fabricator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='app_catalog.Fabricator', verbose_name='производитель')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
    ]
