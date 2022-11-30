import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import OrderCreateForm


logger = logging.getLogger(__name__)


class OrderCreateView(View):
    """ Страница ввода параметров пользователя. """
    def get(self, request):
        """ Метод для GET запроса к странице. """
        form = OrderCreateForm()
        logger.debug('Запрошена страница оформления заказа.')
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа'})

    def post(self, request):
        """ Метод для POST запроса к странице. """
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            logger.debug('Заказ успешно оформлен.')
            return HttpResponseRedirect(reverse('app_ordering:payment'))


class PaymentView(View):
    """ Страница оплаты заказа. """
    def get(self, request):
        """ Метод для GET запроса к странице. """
        logger.debug('Запрошена страница оплаты заказа.')
        return render(request, 'app_ordering/payment.html', {'page_title': 'Оплата'})

    def post(self, request):
        """ Метод для POST запроса к странице. """
        logger.debug('Оплата заказа успешно оформлена.')
        return render(request, 'app_ordering/payment.html', {'page_title': 'Оплата'})


def progress_payment(request):
    """ Страница ожидания оплаты заказа. """
    logger.debug('Запрошена страница ожидания оплаты заказа.')
    return render(request, 'app_ordering/progress_payment.html', {'page_title': 'Ожидание оплаты'})
