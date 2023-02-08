import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView

from .models import Order
from .errors import PaymentError

logger = logging.getLogger(__name__)


class PaymentService(LoginRequiredMixin, APIView):
    """ Сервис оплаты заказа. """
    def post(self, order_id, card_num, order_cost):
        order = Order.objects.get(id=order_id)
        last_digits = ['2', '4', '6', '8']
        if (card_num[8] not in last_digits) or ('x' in card_num):
            order.paid = False
            raise PaymentError()
        order.paid = True
        logger.debug('Заказ №{order_id} успешно оплачен. Сумма заказа {order_cost}$.'.format(order_id=order_id,
                                                                                             order_cost=order_cost))
