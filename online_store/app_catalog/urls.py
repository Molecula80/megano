from django.urls import path

from .views import IndexView, ProductListView, ProductDetailView, CategoryListApi, CategoryDetailApi

app_name = 'app_catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('catalog/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('api/categories/', CategoryListApi.as_view(), name='category_list_api'),
    path('api/categories/<int:pk>/', CategoryDetailApi.as_view(), name='category_detail_api'),
]
