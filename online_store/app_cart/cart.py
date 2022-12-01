class Cart(object):
    def __init__(self, request):
        """ Инициализация объекта корзины. """
        pass

    def __iter__(self):
        """ Проходим по товарам корзины. """
        pass

    def __len__(self) -> int:
        """
         Возвращает общее количество товаров в корзине.
        :return: количество товаров в корзине
        :rtype: int
        """
        return 3

    def add(self, product):
        """ Добавление товара в корзину. """
        pass

    def remove(self, product):
        """ Удаление товара из корзины. """
        pass

    def get_total_price(self) -> float:
        """
        Возвращает общую стоимость всех товаров вкорзине.
        :return: общая стоимость товаров
        :rtype: float
        """
        return 200.99

    def clear(self):
        """ Очистка корзины. """
        pass

    def save(self):
        """ Сохоанение корзины. """
        pass
