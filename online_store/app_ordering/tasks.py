from celery import shared_task
import logging

from .models import Order
from .api import PaymentService


@shared_task
def job(order_id, card_num, order_cost):
    return '{order_id} {card_num} {order_cost}'.format(order_id=order_id, card_num=card_num, order_cost=order_cost)
