from django_filters import FilterSet
from .models import CartItem


class CartItemFilter(FilterSet):
    """ Класс для фильтрации единиц корзины. """
    class Meta:
        model = CartItem
        fields = {
            'user__email': ['exact'],
            'user__full_name': ['exact'],
            'product__title': ['exact'],
            'product__price': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'quantity': ['gt', 'gte', 'exact', 'lte', 'lt'],
        }
