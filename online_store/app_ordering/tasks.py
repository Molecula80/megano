from celery import shared_task
import logging

from .models import Order
from .services import PaymentService

logger = logging.getLogger(__name__)


@shared_task
def job(order_id, card_num):
    order = Order.objects.get(id=order_id)
    order_cost = order.total_cost
    PaymentService.order_payment(order_id=order_id, card_num=card_num, order_cost=order_cost)
