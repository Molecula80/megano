from django_filters import FilterSet

from .models import Order, OrderItem


class OrderFilter(FilterSet):
    """ Класс для фильтрации заказоа. """
    class Meta:
        model = Order
        fields = {
            'user__email': ['exact'],
            'user__full_name': ['exact'],
            'created': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'email': ['exact'],
            'full_name': ['exact'],
            'delivery_method__title': ['exact'],
            'city': ['exact'],
            'payment_method': ['exact'],
            'paid': ['exact'],
            'delivery_price': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'total_cost': ['gt', 'gte', 'exact', 'lte', 'lt'],
        }


class OrderItemFilter(FilterSet):
    """ Класс для фильтрации единицы заказоа. """
    class Meta:
        model = OrderItem
        fields = {
            'order__id': ['exact'],
            'product__title': ['exact'],
            'price': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'quantity': ['gt', 'gte', 'exact', 'lte', 'lt'],
        }
