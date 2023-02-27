from .forms import SearchProductForm
from .models import Category


def categories(request) -> dict:
    """
    Контекстный процессор для категорий товаров.
    :param request:
    :return: словарь, содержащий категории товаров в качестве значения
    :rtype: dict
    """
    return {'categories': Category.objects.filter(active=True).order_by('-sort_index')}


def product_form(request) -> dict:
    """
    Контекстный процессор для формы поиска товаров товаров.
    :param request:
    :return: словарь, содержащий форму поиска товаров
    :rtype: dict
    """
    return {'product_form': SearchProductForm}
