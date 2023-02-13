from django.db import models

from app_users.models import User
from app_catalog.models import Product


class CartItem(models.Model):
    """ Модель товара в корзине. """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items',
                                verbose_name='товар')
    quantity = models.PositiveIntegerField(verbose_name='количество')

    class Meta:
        verbose_name = 'единица корзины'
        verbose_name_plural = 'единицы корзины'

    def __str__(self):
        """ Возвращает email пользователя и название товара. """
        return '{email}, {product}'.format(email=self.user.email, product=self.product.title)
