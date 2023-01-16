import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import OrderCreateForm
from .models import DeliveryMethod
from app_users.forms import RegisterForm, AuthForm
from common.functions import register
from app_cart.cart import Cart
from app_cart.models import CartItem

logger = logging.getLogger(__name__)


class OrderCreateView(LoginRequiredMixin, View):
    """ Страница ввода параметров пользователя. """
    def get(self, request):
        """ Метод для GET запроса к странице. """
        user = request.user
        initial = {'full_name': user.full_name, 'telephone': user.telephone, 'email': user.email}
        form = OrderCreateForm(initial=initial)
        # Строка, содержащте все способы доставки.
        delivery_str = '|'.join(dm.title for dm in DeliveryMethod.objects.all())
        cart = Cart(request)
        logger.debug('Запрошена страница оформления заказа.')
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа',
                                                                  'delivery_str': delivery_str, 'cart': cart})

    def post(self, request):
        """ Метод для POST запроса к странице. """
        form = OrderCreateForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            logger.debug('Заказ успешно оформлен.')
            return HttpResponseRedirect(reverse('app_ordering:payment'))
        if request.is_ajax():
            return render(request, 'app_ordering/order_ajax.html', {'form': form, 'page_title': 'Оформление заказа',
                                                                    'cart': cart})
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа',
                                                                  'cart': cart})


def register_view(request):
    """ Страница регистрации. """
    cart = Cart(request)
    next_page = 'app_ordering:order_create'
    template = 'app_ordering/register.html'
    error = str()
    email_exists = False
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        # Если пользователь с указанным email уже существует, выводим всплывающее окно.
        if register_form.has_error(field='email', code='unique'):
            email_exists = True
        auth_form = AuthForm(request.POST)
        context = {'register_form': register_form, 'auth_form': auth_form, 'page_title': 'Оформление заказа'}
        if register_form.is_valid():
            return register(request=request, next_page=next_page, form=register_form, template=template,
                            context=context)
        elif auth_form.is_valid():
            email = auth_form.cleaned_data['email']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    # Удаляем корзину пользователя из базы данных.
                    auth_cart = CartItem.objects.filter(user=user)
                    cart.delete_cart_from_database(auth_cart)
                    logger.debug('Пользователь {} вошел в систему.'.format(email))
                    return HttpResponseRedirect(reverse('app_ordering:order_create'))
                else:
                    error = 'Ошибка! Аккаунт пользователя неактивен.'
            else:
                error = 'Ошибка! Проверьте правильность написания email и пароля.'
    else:
        register_form = RegisterForm()
        auth_form = AuthForm()
    if request.is_ajax():
        return render(request, 'app_ordering/popups.html', {'register_form': register_form, 'auth_form': auth_form,
                                                            'page_title': 'Оформление заказа', 'error': error,
                                                            'email_exists': email_exists})
    return render(request, 'app_ordering/register.html', {'register_form': register_form, 'auth_form': auth_form,
                                                          'page_title': 'Оформление заказа', 'error': error,
                                                          'email_exists': email_exists})


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
