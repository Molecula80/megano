import logging
from rest_framework.generics import GenericAPIView
from .errors import PaymentError

logger = logging.getLogger(__name__)


class PaymentService(GenericAPIView):
    """ Сервис оплаты заказа. """
    @classmethod
    def order_payment(cls, order_id, card_num, order_sum):
        """ Оплата заказа. """
        last_digits = ['2', '4', '6', '8']
        if (card_num[8] not in last_digits) or ('x' in card_num):
            raise PaymentError()
