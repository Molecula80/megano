import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST

from .forms import OrderCreateForm
from .models import DeliveryMethod
from app_users.forms import RegisterForm, AuthForm
from common.functions import register
from common.decorators import ajax_required
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
        cart = Cart(request)
        logger.debug('Запрошена страница оформления заказа.')
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа',
                                                                  'cart': cart})

    def post(self, request):
        """ Метод для POST запроса к странице. """
        form = OrderCreateForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')
            logger.debug('Способ оплаты: {}'.format(payment_method))
            if payment_method == '1':
                return HttpResponseRedirect(reverse('app_ordering:payment'))
            return HttpResponseRedirect(reverse('app_ordering:payment_someone'))
        if request.is_ajax():
            return render(request, 'app_ordering/order_ajax.html', {'form': form, 'page_title': 'Оформление заказа',
                                                                    'cart': cart})
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа',
                                                                  'cart': cart})


@ajax_required
@require_POST
def get_delivery_method(request):
    """ Получение способа доставки. """
    cart = Cart(request)
    delivery_val = request.POST.get('delivery_val')
    try:
        delivery_method = DeliveryMethod.objects.all()[int(delivery_val) - 1]
        delivery_price = delivery_method.get_delivery_price(total_price=cart.total_price)
        order_price = cart.total_price + delivery_price
        return JsonResponse({'delivery_method': delivery_method.title, 'delivery_price': delivery_price,
                             'order_price': order_price})
    except:
        pass
    return JsonResponse({'status': 'ok'})


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
        logger.debug('Запрошена страница оплаты заказа онлайн картой.')
        return render(request, 'app_ordering/payment.html', {'page_title': 'Оплата', 'label': 'Номер карты'})

    def post(self, request):
        """ Метод для POST запроса к странице. """
        logger.debug('Оплата заказа успешно оформлена.')
        return render(request, 'app_ordering/payment.html', {'page_title': 'Оплата', 'label': 'Номер карты'})


class PaymentSomeoneView(PaymentView):
    """ Страница оплаты заказа. """
    def get(self, request):
        """ Метод для GET запроса к странице. """
        return render(request, 'app_ordering/payment.html', {'page_title': 'Оплата', 'label': 'Номер счета',
                                                             'p_someone': True})


@login_required
def progress_payment(request):
    """ Страница ожидания оплаты заказа. """
    logger.debug('Запрошена страница ожидания оплаты заказа.')
    return render(request, 'app_ordering/progress_payment.html', {'page_title': 'Ожидание оплаты'})
