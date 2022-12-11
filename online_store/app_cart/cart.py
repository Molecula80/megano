from decimal import Decimal
from typing import Iterable
from django.conf import settings

from app_catalog.models import Product


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

    def add(self, product: Product, quantity: int = 1, update_quantity: bool = False) -> None:
        """ Добавление товара в корзину или обновление его количества. """
        product_id = str(product.id)
        if product_id not in self.__cart:
            self.__cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.__cart[product_id]['quantity'] = quantity
        else:
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
        self.__cart[str(product_id)]['quantity'] += quantity
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
