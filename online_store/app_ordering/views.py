import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import OrderCreateForm
from app_users.forms import RegisterForm, AuthForm
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
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        auth_form = AuthForm(request.POST)
        if register_form.is_valid():
            return register(request=request, next_page=next_page, form=register_form)
    else:
        register_form = RegisterForm()
        auth_form = AuthForm()
    if request.is_ajax():
        return render(request, 'app_ordering/popups.html', {'register_form': register_form, 'auth_form': auth_form,
                                                            'page_title': 'Оформление заказа'})
    return render(request, 'app_ordering/register.html', {'register_form': register_form, 'auth_form': auth_form,
                                                          'page_title': 'Оформление заказа'})


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
