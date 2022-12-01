import logging

from django.http import HttpResponse
from django.shortcuts import render

from .cart import Cart


logger = logging.getLogger(__name__)


def cart_detail(request):
    """ Страница корзины. """
    cart = Cart(request)
    logger.debug('Запрошена страница корзины.')
    return render(request, 'app_cart/cart_detail.html', {'cart': cart, 'page_title': 'Корзина'})


def cart_add(request):
    """ Добавление товара в корзину. """
    return HttpResponse('Товар успешно добавлен в корзину.')


def cart_remove(request):
    """ Удаление товара из корзины. """
    return HttpResponse('Товар успешно удален из корзины.')
