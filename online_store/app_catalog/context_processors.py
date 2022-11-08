from .models import Category


def categories(request) -> dict:
    """
    Контекстный процессор для передачи шести категорий товаров в футтер сайта.
    :param request:
    :return: словарь, содержащий шесть категорий в качестве значения
    :rtype: dict
    """
    return {'categories': Category.objects.filter(active=True).order_by('-sort_index')}
