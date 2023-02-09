from celery import shared_task


@shared_task
def job(order_id, card_num, order_cost):
    return '{order_id} {card_num} {order_cost}'.format(order_id=order_id, card_num=card_num, order_cost=order_cost)
