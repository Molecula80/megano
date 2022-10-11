from django_filters import FilterSet
from .models import Category


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'parent__title': ['exact'],
            'title': ['exact'],
            'sort_index': ['gt', 'gte', 'exact', 'lte', 'lt'],
            'active': ['exact'],
        }
