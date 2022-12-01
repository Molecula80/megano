from .cart import Cart


def cart(request) -> dict:
    """
    Контекстный процессор для объекта корзины.
    :param request:
    :return: словарь, содержащий объект корзины в качестве значения
    :rtype: dict
    """
    return {'cart': Cart(request)}
