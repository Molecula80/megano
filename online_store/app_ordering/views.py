import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import OrderCreateForm
from common.functions import register

logger = logging.getLogger(__name__)


class OrderCreateView(LoginRequiredMixin, View):
    """ Страница ввода параметров пользователя. """
    def get(self, request):
        """ Метод для GET запроса к странице. """
        user = request.user
        initial = {'full_name': user.full_name, 'telephone': user.telephone, 'email': user.email}
        form = OrderCreateForm(initial=initial)
        logger.debug('Запрошена страница оформления заказа.')
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа'})

    def post(self, request):
        """ Метод для POST запроса к странице. """
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            logger.debug('Заказ успешно оформлен.')
            return HttpResponseRedirect(reverse('app_ordering:payment'))
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа'})


def register_view(request):
    """ Страница регистрации. """
    next_page = 'app_ordering:order_create'
    template = 'app_ordering/register.html'
    page_title = 'Оформление заказа'
    return register(request=request, next_page=next_page, template=template, page_title=page_title)


class PaymentView(LoginRequiredMixin, View):
    """ Страница оплаты заказа. """
    def get(self, request):
        """ Метод для GET запроса к странице. """
        logger.debug('Запрошена страница оплаты заказа.')
        return render(request, 'app_ordering/payment.html', {'page_title': 'Оплата'})

    def post(self, request):
        """ Метод для POST запроса к странице. """
        logger.debug('Оплата заказа успешно оформлена.')
        return render(request, 'app_ordering/payment.html', {'page_title': 'Оплата'})


@login_required
def progress_payment(request):
    """ Страница ожидания оплаты заказа. """
    logger.debug('Запрошена страница ожидания оплаты заказа.')
    return render(request, 'app_ordering/progress_payment.html', {'page_title': 'Ожидание оплаты'})
