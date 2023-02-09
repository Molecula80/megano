from decimal import Decimal
from typing import Iterable
from django.conf import settings

from app_catalog.models import Product
from app_users.models import User
from .models import CartItem


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

    def merge_carts(self, auth_cart) -> None:
        """
        Слияние корзин анонимного и аутентифицированного пользователя, после того как последний вошел в систему.
        """
        # Добавляем в корзину продукты из базы данных.
        for item in auth_cart:
            product = item.product
            quantity = item.quantity
            self.add(product=product, quantity=quantity)

    @classmethod
    def delete_cart_from_database(cls, auth_cart) -> None:
        """ Удаление корзины из базы данных, после того как пользователь вошел в систему. """
        auth_cart.delete()

    def add(self, product: Product, quantity: int = 1) -> None:
        """ Добавление товара в корзину или обновление его количества. """
        product_id = str(product.id)
        if product_id not in self.__cart:
            self.__cart[product_id] = {'quantity': 0, 'price': str(product.price),
                                       'free_delivery': product.free_delivery}
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

    @property
    def total_price(self) -> float:
        """
        Геттер. Возвращает общую стоимость всех товаров вкорзине.
        :return: общая стоимость товаров
        :rtype: float
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.__cart.values())

    @property
    def free_delivery(self) -> bool:
        """
        Геттер. Возвращает True, если у всех товаров в корзине свободная доставка. В противном случае возвращает False.
        """
        for item in self.__cart.values():
            if not item['free_delivery']:
                return False
        return True

    def clear(self) -> None:
        """ Очистка корзины. """
        del self.__session[settings.CART_SESSION_ID]
        self.save()

    def save(self) -> None:
        """ Сохоанение корзины. """
        # Помечаем сессию как измененную.
        self.__session.modified = True

    def save_cart_in_database(self, user: User) -> None:
        """ Сохранетие корзины в базе данных, при выходе пользователя пользователя из системы. """
        cart_items = []
        for key, value in self.__cart.items():
            product = Product.objects.get(id=int(key))
            quantity = value['quantity']
            cart_items.append(CartItem(user=user, product=product, quantity=quantity))
        CartItem.objects.bulk_create(cart_items)
