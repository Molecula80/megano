from django_filters import FilterSet

from .models import Category, Product


class CategoryFilter(FilterSet):
    """ Класс для фильтрации категорий товаров. """
    class Meta:
        model = Category
        fields = {
            'parent__title': ['exact'],
            'title': ['exact'],
            'sort_index': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'active': ['exact'],
        }


class ProductFilter(FilterSet):
    """ Класс для фильтрации товаров. """
    class Meta:
        model = Product
        fields = {
            'fabricator__title': ['exact'],
            'title': ['exact'],
            'slug': ['exact'],
            'price': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'added_at': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'num_purchases': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'sort_index': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'in_stock': ['exact'],
            'free_delivery': ['exact'],
            'limited_edition': ['exact'],
        }
