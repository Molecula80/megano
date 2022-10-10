from django.urls import path

from .views import IndexView, CategoryList

app_name = 'app_catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/categories/', CategoryList.as_view(), name='category_list'),
]
