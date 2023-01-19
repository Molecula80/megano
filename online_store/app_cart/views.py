import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST

from app_catalog.models import Product
from common.decorators import ajax_required

from .cart import Cart
from .forms import CartAddProductForm


logger = logging.getLogger(__name__)


def cart_detail(request):
    """ Страница корзины. """
    cart = Cart(request)
    logger.debug('Запрошена страница корзины.')
    return render(request, 'app_cart/cart_detail.html', {'cart': cart, 'page_title': 'Корзина'})


class CartAdd(View):
    """ Добавление товара в корзину. """
    def get(self, request, product_id: int):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=1)
        logger.debug('Товар {} добавлен в корзину методом GET.'.format(product.title))
        return redirect('app_cart:cart_detail')

    def post(self, request, product_id: int):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            cart.add(product=product, quantity=quantity)
            logger.debug('Товар {} добавлен в корзину методом POST.'.format(product.title))
        return redirect('app_cart:cart_detail')


def cart_remove(request, product_id: int):
    """ Удаление товара из корзины. """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    logger.debug('Товар {} удален из корзины.'.format(product.title))
    return redirect('app_cart:cart_detail')


@ajax_required
@require_POST
def cart_update(request):
    """ Изменение количества товара в корзине. """
    cart = Cart(request)
    product_id = request.POST.get('id')
    quantity = request.POST.get('quantity')
    try:
        quantity = int(quantity)
        cart.update(product_id=product_id, quantity=quantity)
        return JsonResponse({'status': 'ok'})
    except:
        pass
    return JsonResponse({'status': 'ok'})
