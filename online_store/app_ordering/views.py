import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST

from app_cart.cart import Cart
from app_cart.models import CartItem
from app_catalog.models import Product
from app_users.forms import AuthForm, RegisterForm
from common.decorators import ajax_required
from common.functions import register

from .forms import OrderCreateForm, PaymentForm
from .models import DeliveryMethod, Order, OrderItem

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
            telephone_str = form.cleaned_data.get('telephone')
            # Оставляем все цифры, кроме семёрки.
            telephone = ''.join(sym for sym in telephone_str[3:] if sym.isdigit())
            if telephone and len(telephone) < 10:
                form.add_error('telephone', 'Это значение недопустимо.')
            else:
                order = form.save(commit=False)
                order.user = request.user
                order.telephone = telephone
                order.delivery_price = request.session.get('delivery_price')
                order.total_cost = request.session.get('order_price')
                order.save()
                logger.debug('Заказ № {} успешно создан.'.format(order.id))
                self.create_order_items(cart=cart, order=order)
                cart.clear()
                if order.payment_method == '1':
                    return HttpResponseRedirect(reverse('app_ordering:payment', args=[order.id]))
                return HttpResponseRedirect(reverse('app_ordering:payment_someone', args=[order.id, 'someone']))
        if request.is_ajax():
            return render(request, 'app_ordering/order_ajax.html', {'form': form, 'page_title': 'Оформление заказа',
                                                                    'cart': cart})
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа',
                                                                  'cart': cart})

    @classmethod
    def create_order_items(cls, cart, order):
        """ Создает единицы заказа. """
        item_list = list()
        for item in cart:
            item_list.append(OrderItem(order=order, product=item['product'], price=item['total_price'],
                                       quantity=item['quantity']))
        OrderItem.objects.bulk_create(item_list)


@ajax_required
@require_POST
def get_delivery_method(request):
    """ Получение способа доставки. """
    cart = Cart(request)
    # Значение способа доставки равно 1 или 2.
    delivery_val = request.POST.get('delivery_val')
    try:
        delivery_method = DeliveryMethod.objects.all()[int(delivery_val) - 1]
        delivery_price = cart.get_delivery_price(d_method=delivery_method)
        order_price = cart.total_price + delivery_price
        # Сохраняем цену доставки и сумарную цену заказа в сессии
        request.session['delivery_price'] = str(delivery_price)
        request.session['order_price'] = str(order_price)
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
        auth_form = AuthForm(request.POST)  # Всплывающее окно с формой для входа.
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
    def get(self, request, order_id, someone=None):
        """ Метод для GET запроса к странице. """
        logger.debug('Запрошена страница оплаты заказа онлайн картой.')
        form = PaymentForm()
        return render(request, 'app_ordering/payment.html', {'page_title': 'Оплата', 'form': form,
                                                             'label': 'Номер карты', 'someone': someone})

    def post(self, request, order_id, someone=None):
        """ Метод для POST запроса к странице. """
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_num = form.cleaned_data.get('card_num')
            logger.debug('Номер карты: {}'.format(card_num))
            self.pay_order(order_id=order_id, card_num=card_num)
            return HttpResponseRedirect(reverse('app_ordering:progress_payment', args=[order_id]))
        if request.is_ajax():
            return render(request, 'app_ordering/payment_ajax.html', {'page_title': 'Оплата', 'form': form,
                                                                      'label': 'Номер карты', 'someone': someone})
        return render(request, 'app_ordering/payment.html', {'page_title': 'Оплата', 'form': form,
                                                             'label': 'Номер карты', 'someone': someone})

    def pay_order(self, order_id, card_num):
        """ Оплата товара. """
        order = Order.objects.select_related('user', 'delivery_method').get(id=order_id)
        # Если номер нечетный или заканчивается на ноль, вызываем ошибку оплаты.
        last_digits = ['2', '4', '6', '8']
        if (card_num[8] not in last_digits) or ('x' in card_num):
            order.paid = False
            order.error_message = 'Ошибка оплаты. Номер карты должен быь четным и не оканчиваться на ноль.'
        else:
            order.paid = True
        order.save()
        # Если заказ успешно оплачен, увеличиваем количество покупок для каждого товара.
        self.buy_products(order)
        logger.debug('Заказ №{order_id} успешно оплачен. Сумма заказа {order_cost}$.'.format(
            order_id=order_id, order_cost=order.total_cost))

    @classmethod
    def buy_products(cls, order):
        """ Увеличение параметра "Количество покупок" для каждого купленного товара. """
        items = order.items.select_related('order', 'product').all()
        products = [item.product for item in items]
        for item in items:
            item.product.num_purchases += item.quantity
        Product.objects.bulk_update(products, fields=['num_purchases'])


@login_required
def progress_payment(request, order_id):
    """ Страница ожидания оплаты заказа. """
    logger.debug('Запрошена страница ожидания оплаты заказа.')
    order = Order.objects.get(id=order_id)
    return render(request, 'app_ordering/progress_payment.html', {'page_title': 'Ожидание оплаты', 'order': order})
