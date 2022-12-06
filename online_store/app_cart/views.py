import logging
from django.shortcuts import render, redirect, get_object_or_404

from app_catalog.models import Product
from .cart import Cart
from .forms import CartAddProductForm


logger = logging.getLogger(__name__)


def cart_detail(request):
    """ Страница корзины. """
    cart = Cart(request)
    prices = list()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        prices.append(item['price'])
    if request.is_ajax():
        return render(request, 'app_cart/item_quantity_ajax.html', {'cart': cart, 'page_title': 'Корзина',
                                                                    'prices': prices})
    logger.debug('Запрошена страница корзины.')
    return render(request, 'app_cart/cart_detail.html', {'cart': cart, 'page_title': 'Корзина', 'prices': prices})


def cart_add(request, product_id: int):
    """ Добавление товара в корзину. """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    logger.debug('Товар {} добавлен в корзину.'.format(product.title))
    return redirect('app_cart:cart_detail')


def cart_remove(request, product_id: int):
    """ Удаление товара из корзины. """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    logger.debug('Товар {} удален из корзины.'.format(product.title))
    return redirect('app_cart:cart_detail')
