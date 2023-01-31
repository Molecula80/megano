import logging
from rest_framework.generics import GenericAPIView

from .models import Order
from .errors import PaymentError

logger = logging.getLogger(__name__)


class PaymentService(GenericAPIView):
    """ Сервис оплаты заказа. """
    @classmethod
    def order_payment(cls, order_id, card_num, order_cost):
        """ Оплата заказа. """
        order = Order.objects.get(id=order_id)
        try:
            last_digits = ['2', '4', '6', '8']
            if (card_num[8] not in last_digits) or ('x' in card_num):
                raise PaymentError()
            order.paid = True
        except PaymentError:
            order.paid = False
            order.error_message = 'Номер карты должен быть чётным и не заканчиваться на ноль.'
        finally:
            order.save(update_fields=['paid'])

