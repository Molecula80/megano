import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import OrderCreateForm
from app_users.forms import RegisterForm
from app_users.models import User


logger = logging.getLogger(__name__)


class OrderCreateView(View):
    """ Страница ввода параметров пользователя. """
    def get(self, request):
        """ Метод для GET запроса к странице. """
        user = request.user
        if user.is_authenticated:
            initial = {'full_name': user.full_name, 'telephone': user.telephone, 'email': user.email}
            form = OrderCreateForm(initial=initial)
        else:
            form = RegisterForm()
        logger.debug('Запрошена страница оформления заказа.')
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа'})

    def post(self, request):
        """ Метод для POST запроса к странице. """
        if request.user.is_authenticated:
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                logger.debug('Заказ успешно оформлен.')
                return HttpResponseRedirect('app_ordering:payment')
        else:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                telephone_str = form.cleaned_data.get('telephone')
                # Оставляем все цифры, кроме семёрки.
                telephone = ''.join(sym for sym in telephone_str[3:] if sym.isdigit())
                if telephone and len(telephone) < 10:
                    form.add_error('telephone', 'Это значение недопустимо.')
                # Если был введен номер телефона, и пользователь с указанным номером телефона уже есть,
                # выводим сообщение об ошибке.
                elif telephone and User.objects.only('telephone').filter(telephone=telephone).exists():
                    form.add_error('telephone', 'Пользователь с таким номером телефона уже есть.')
                else:
                    user.telephone = telephone
                    user.save()
                    email = form.cleaned_data.get('email')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(email=email, password=raw_password)
                    login(request, user)
                    logger.debug('Пользователь {} зарегистрировался на сайте.'.format(email))
                    return HttpResponseRedirect('app_ordering:order_create#step2')


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
