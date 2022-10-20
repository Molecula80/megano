from django.db import models
from django.urls import reverse


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
    """ Модель производителя. """
    title = models.CharField(max_length=255, verbose_name='название')

    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'

    def __str__(self):
        return self.title


class Product(models.Model):
    """ Модель товара. """
    fabricator = models.ForeignKey(Fabricator, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='products', verbose_name='производитель')
    categories = models.ManyToManyField(Category, related_name='products', verbose_name='категории')
    title = models.CharField(max_length=255, verbose_name='название')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    image = models.ImageField(upload_to='images/products/', blank=True, null=True, verbose_name='иконка')
    added_at = models.DateTimeField(verbose_name='дата публикации')
    num_purchases = models.PositiveIntegerField(default=0, verbose_name='количество покупок')
    sort_index = models.PositiveIntegerField(verbose_name='индекс сортировки')
    in_stock = models.BooleanField(default=False, verbose_name='в наличии')
    free_delivery = models.BooleanField(default=False, verbose_name='с бесплатной доставкой')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченный тираж')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('app_catalog:product_detail', args=[self.slug])


class DescrPoint(models.Model):
    """ Модель пункта описания товара. """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='descr_points', verbose_name='товар')
    content = models.CharField(max_length=255, verbose_name='содержание')

    class Meta:
        verbose_name = 'пункт описания'
        verbose_name_plural = 'пункты описания'

    def __str__(self):
        return self.content


class AddInfoPoint(models.Model):
    """ Модель пункта дополнительной информации о товаре. """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='add_info_points', verbose_name='товар')
    characteristic = models.CharField(max_length=255, verbose_name='характеристика')
    value = models.CharField(max_length=255, verbose_name='значение')

    class Meta:
        verbose_name = 'пункт доп. информации'
        verbose_name_plural = 'пункты доп. информации'

    def __str__(self):
        return '{characteristic}: {value}'.format(characteristic=self.characteristic, value=self.value)
