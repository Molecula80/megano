from celery import shared_task
import logging

from .services import PaymentService

logger = logging.getLogger(__name__)


@shared_task
def job(order_id, card_num, order_sum):
    PaymentService.order_payment(order_id=order_id, card_num=card_num, order_sum=order_sum)
