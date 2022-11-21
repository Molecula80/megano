from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.core.cache import cache

from app_users.models import User


class Category(models.Model):
    """ Модель категории товаров. """
    parent = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, related_name='children',
                               verbose_name='родитель')
    title = models.CharField(max_length=255, verbose_name='название')
    sort_index = models.PositiveIntegerField(verbose_name='индекс сортировки')
    image = models.ImageField(upload_to='images/categories/', blank=True, null=True, verbose_name='изображение')
    icon = models.FileField(upload_to='images/icons/', blank=True, null=True, verbose_name='иконка')
    active = models.BooleanField(default=False, verbose_name='активно')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        """
        Возвращает название каегории товаров.
        :return: название категории
        :rtype: str
        """
        return str(self.title)


class Seller(models.Model):
    """ Модель продавца."""
    name = models.CharField(max_length=255, verbose_name='имя')

    class Meta:
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'

    def __str__(self) -> str:
        """
        Возвращает имя продавца.
        :return: имя продавца
        :rtype: str
        """
        return str(self.name)


class Fabricator(models.Model):
    """ Модель производителя. """
    title = models.CharField(max_length=255, verbose_name='название')

    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'

    def __str__(self) -> str:
        """
        Возвращает название производителя.
        :return: название производителя
        :rtype: str
        """
        return str(self.title)


class Product(models.Model):
    """ Модель товара. """
    seller = models.ForeignKey(Seller, blank=True, null=True, on_delete=models.SET_NULL, related_name='products',
                               verbose_name='продавец')
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
    active = models.BooleanField(default=False, verbose_name='активно')
    in_stock = models.BooleanField(default=False, verbose_name='в наличии')
    free_delivery = models.BooleanField(default=False, verbose_name='с бесплатной доставкой')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченный тираж')

    class Meta:
        ordering = ['id']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self) -> str:
        """
        Возвращает название товара.
        :return: название товара
        :rtype: str
        """
        return str(self.title)

    def get_absolute_url(self) -> str:
        """
        Возвращает url детальной страницы товара.
        :return: url детальной страницы товара
        :rtype str
        """
        return reverse('app_catalog:product_detail', args=[self.slug])


class DescrPoint(models.Model):
    """ Модель пункта описания товара. """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='descr_points', verbose_name='товар')
    content = models.CharField(max_length=255, verbose_name='содержание')

    class Meta:
        verbose_name = 'пункт описания'
        verbose_name_plural = 'пункты описания'

    def __str__(self) -> str:
        """
        Возвращает содержание пункта описания товара.
        :return: содержание пункта описания
        :rtype: str
        """
        return str(self.content)


class AddInfoPoint(models.Model):
    """ Модель пункта дополнительной информации о товаре. """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='add_info_points', verbose_name='товар')
    characteristic = models.CharField(max_length=255, verbose_name='характеристика')
    value = models.CharField(max_length=255, verbose_name='значение')

    class Meta:
        verbose_name = 'пункт доп. информации'
        verbose_name_plural = 'пункты доп. информации'

    def __str__(self) -> str:
        """
        Возвращает характеристику товара и ее значение.
        :return: характеристика товара и ее значение
        :rtype: str
        """
        return '{characteristic}: {value}'.format(characteristic=self.characteristic, value=self.value)


class Review(models.Model):
    """ Модель отзыва о товаре. """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='пользователь')
    name = models.CharField(max_length=255, verbose_name='имя')
    email = models.EmailField()
    text = models.TextField(verbose_name='текст')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='дата написания')
    active = models.BooleanField(default=True, verbose_name='активно')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self) -> str:
        """
        Возаращает название товара, имя автора и дату написания отзыва.
        :return: название товара, имя автора и дату написания отзыва
        :rtype: str
        """
        return '{product} {name} {added_at}'.format(product=self.product, name=self.name, added_at=self.added_at)


def clear_cache(*args, **kwargs):
    """ Сбрасывает кеш при изменении товара. """
    keys = ['page_title', 'categories', 'descr_points', 'add_info_points', 'num_reviews']
    cache.delete_many(keys)


post_save.connect(clear_cache, sender=Product)
