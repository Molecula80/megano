from django.db import models


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
