class Cart(object):
    def __init__(self, request):
        """ Инициализация объекта корзины. """
        pass

    def __iter__(self):
        """ Проходим по товарам корзины. """
        pass

    def __len__(self):
        """ Возвращает общее количество товаров в корзине. """
        return 3

    def add(self, product):
        """ Добавление товара в корзину. """
        pass

    def remove(self, product):
        """ Удаление товара из корзины. """
        pass

    def get_total_price(self):
        """ Возвращает общую стоимость всех товаров вкорзине. """
        return 200.99

    def clear(self):
        """ Очистка корзины. """
        pass

    def save(self):
        pass
