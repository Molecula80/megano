from django.db import models


class Order(models.Model):
    """ Модель заказа. """
    date = models.DateField(auto_now_add=True, verbose_name='дата заказа')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    telephone = models.CharField(max_length=16, blank=True, null=True, verbose_name='телефон')
    email = models.EmailField(unique=True)
    delivery_method = models.ForeignKey('DeliveryMethod', null=True, on_delete=models.SET_NULL, related_name='orders',
                                        verbose_name='способ доставки')
    city = models.CharField(max_length=255, verbose_name='город')
    address = models.TextField(verbose_name='адрес')


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

    def get_delivery_price(self, total_price):
        """ Получение стоимости доставки. """
        if self.free_delivery_cost and total_price >= self.free_delivery_cost:
            return 0
        return self.price
