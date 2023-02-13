import logging

from .models import Order
from .errors import PaymentError
from app_catalog.models import Product

logger = logging.getLogger(__name__)


class PaymentService:
    """ Сервис оплаты заказа. """
    def __init__(self, order_id, card_num, order_cost):
        self.__order_id = order_id
        self.__card_num = card_num
        self.__order_cost = order_cost

    def pay_order(self):
        order = Order.objects.select_related('user', 'delivery_method').get(id=self.__order_id)
        last_digits = ['2', '4', '6', '8']
        if (self.__card_num[8] not in last_digits) or ('x' in self.__card_num):
            order.paid = False
            order.error_message = 'Ошибка оплаты. Номер карты должен быь четным и не оканчиваться на ноль.'
            order.save()
            raise PaymentError()
        order.paid = True
        order.save()
        self.buy_products(order)
        logger.debug('Заказ №{order_id} успешно оплачен. Сумма заказа {order_cost}$.'.format(
            order_id=self.__order_id, order_cost=self.__order_cost))

    @classmethod
    def buy_products(cls, order):
        """ Покупка товаров. """
        items = order.items.select_related('order', 'product').all()
        products = [item.product for item in items]
        for item in items:
            item.product.num_purchases += item.quantity
        Product.objects.bulk_update(products, fields=['num_purchases'])

