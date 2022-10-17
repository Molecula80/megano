from django.db import models


class Category(models.Model):
    """ Модель категории товаров. """
    parent = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, related_name='children',
                               verbose_name='родитель')
    title = models.CharField(max_length=255, verbose_name='название')
    sort_index = models.PositiveIntegerField(verbose_name='индекс сортировки')
    icon = models.ImageField(upload_to='images/categories/', blank=True, null=True, verbose_name='иконка')
    active = models.BooleanField(default=False, verbose_name='активно')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Fabricator(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')

    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'

    def __str__(self):
        return self.title


class Product(models.Model):
    """ Модель товара. """
    categories = models.ManyToManyField(Category, related_name='products', verbose_name='категории')
    fabricator = models.ForeignKey(Fabricator, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='products', verbose_name='производитель')
    title = models.CharField(max_length=255, verbose_name='название')
    slug = models.SlugField(max_length=255, unique_for_date='added_at')
    description = models.CharField(max_length=100, verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    num_purchases = models.PositiveIntegerField(default=0, verbose_name='количество покупок')
    image = models.ImageField(upload_to='images/products/', blank=True, null=True, verbose_name='иконка')
    sort_index = models.PositiveIntegerField(verbose_name='индекс сортировки')
    in_stock = models.BooleanField(default=False, verbose_name='в наличии')
    free_delivery = models.BooleanField(default=False, verbose_name='с бесплатной доставкой')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченный тираж')
    added_at = models.DateTimeField(verbose_name='дата публикации')
