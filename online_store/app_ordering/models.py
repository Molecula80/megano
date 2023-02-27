from django.db import models

from app_catalog.models import Product
from app_users.models import User


class Order(models.Model):
    """ Модель заказа. """
    PAYMENT_METHOD_CHOICES = [('1', 'Онлайн картой'), ('2', 'Онлайн со случайного чужого счета')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='пользователь')
    created = models.DateField(auto_now_add=True, verbose_name='дата заказа')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    telephone = models.CharField(max_length=16, verbose_name='телефон')
    email = models.EmailField()
    delivery_method = models.ForeignKey('DeliveryMethod', on_delete=models.CASCADE, related_name='orders',
                                        verbose_name='способ доставки')
    city = models.CharField(max_length=255, verbose_name='город')
    address = models.TextField(verbose_name='адрес')
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES, default=1,
                                      verbose_name='способ оплаты')
    comment = models.TextField(blank=True, null=True, verbose_name='комментарий')
    paid = models.NullBooleanField(default=None, verbose_name='оплачено')
    error_message = models.TextField(blank=True, null=True, default=str(), verbose_name='сообщение об ошибке')
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='стоимость доставки')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='итоговая стоимость')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        """ Возвращает ID заказа. """
        return '{}'.format(self.id)


class OrderItem(models.Model):
    """ Модель единицы заказа. """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name='товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    quantity = models.PositiveIntegerField(verbose_name='количество')

    class Meta:
        verbose_name = 'единица заказа'
        verbose_name_plural = 'единицы заказа'

    def __str__(self):
        """ Возвращает ID заказа и название продукта. """
        return '{order}, {product}'.format(order=self.order.id, product=self.product.title)


class DeliveryMethod(models.Model):
    """ Модель способа доставки. """
    title = models.CharField(max_length=20, verbose_name='название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='стоимость')
    free_delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                             verbose_name='стоимость заказа, после которой действует '
                                                          'бесплатная доставка')

    class Meta:
        verbose_name = 'способ доставки'
        verbose_name_plural = 'спопобы доставки'

    def __str__(self) -> str:
        """ Возвращает название способа доставки. """
        return '{}'.format(self.title)
