from decimal import Decimal
from typing import Iterable
from django.conf import settings

from app_catalog.models import Product
from django.http import HttpResponse


class Cart(object):
    def __init__(self, request) -> None:
        """ Инициализация объекта корзины. """
        self.__session = request.session
        cart = self.__session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем сессии в пустую корзину.
            cart = self.__session[settings.CART_SESSION_ID] = dict()
        self.__cart = cart

    def __iter__(self) -> Iterable:
        """ Проходим по товарам корзины и получаем соответствующие объекты Product. """
        product_ids = self.__cart.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        products = Product.objects.filter(id__in=product_ids)
        cart = self.__cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:
        """
         Возвращает общее количество товаров в корзине.
        :return: количество товаров в корзине
        :rtype: int
        """
        return sum(item['quantity'] for item in self.__cart.values())

    def merge_carts(self, request, user):
        """
        Слияние корзин анонимного и аутентифицированного пользователя, после того как последний вошел в систему.
        """
        cookie_name = 'cart_{}'.format(user.id)
        auth_cart = request.COOKIES.get(cookie_name)
        if not auth_cart:
            auth_cart = str()
        try:
            for str_product in auth_cart.split(', '):
                product_id = int(str_product.split(', ')[0])
                product = Product.objects.get(id=product_id)
                quantity = int(str_product.split(', ')[1])
                self.add(product=product, quantity=quantity)
        except ValueError:
            pass

    def add(self, product: Product, quantity: int = 1) -> None:
        """ Добавление товара в корзину или обновление его количества. """
        product_id = str(product.id)
        if product_id not in self.__cart:
            self.__cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.__cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product: Product) -> None:
        """ Удаление товара из корзины. """
        product_id = str(product.id)
        if product_id in self.__cart:
            del self.__cart[product_id]
            self.save()

    def update(self, product_id: int, quantity: int) -> None:
        """ Изменение количества товара в корзине. """
        product_id = str(product_id)
        self.__cart[product_id]['quantity'] = quantity
        if quantity == 0:
            product = Product.objects.get(id=product_id)
            return self.remove(product)
        self.save()

    def get_total_price(self) -> float:
        """
        Возвращает общую стоимость всех товаров вкорзине.
        :return: общая стоимость товаров
        :rtype: float
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.__cart.values())

    def clear(self) -> None:
        """ Очистка корзины. """
        del self.__session[settings.CART_SESSION_ID]
        self.save()

    def save(self) -> None:
        """ Сохоанение корзины. """
        # Помечаем сессию как измененную.
        self.__session.modified = True

    def cart_cookie(self, request):
        """ Сохранение корзины в файле cookie при выходе пользователя из системы. """
        response = HttpResponse('cart')
        name = 'cart_{}'.format(request.user.id)
        value = ', '.join(list(self.get_cookie_value()))
        two_weeks = 14 * 24 * 60 * 60
        response.set_cookie(name, value, two_weeks)
        return response

    def get_cookie_value(self) -> Iterable:
        """ Возвращает итератор, содержащий id и количество всех продуктов в корзине. """
        for key, value in self.__cart.items():
            quantity = value['quantity']
            yield '{id} {quantity}'.format(id=key, quantity=quantity)
