# Generated by Django 2.2 on 2023-01-09 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='стоимость')),
                ('free_delivery_cost', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='стоимость заказа, после которой действует бесплатная доставка')),
            ],
            options={
                'verbose_name': 'способ доставки',
                'verbose_name_plural': 'спопобы доставки',
            },
        ),
    ]