from django.urls import path

from .views import IndexView, ProductListView, ProductDetailView
from .api import CategoryListApi, CategoryDetailApi, FabricatorListApi, FabricatorDetailApi, ProductListApi, \
    ProductDetailApi, DescrPointListApi, DescrPointDetailApi, AddInfoPointListApi, AddInfoPointDetailApi

app_name = 'app_catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('catalog/<slug>/', ProductDetailView.as_view(), name='product_detail'),
    # API
    path('api/categories/', CategoryListApi.as_view(), name='category_list_api'),
    path('api/categories/<int:pk>/', CategoryDetailApi.as_view(), name='category_detail_api'),
    path('api/fabricators/', FabricatorListApi.as_view(), name='fabricator_list_api'),
    path('api/fabricators/<int:pk>/', FabricatorDetailApi.as_view(), name='fabricator_detail_api'),
    path('api/products/', ProductListApi.as_view(), name='product_list_api'),
    path('api/products/<int:pk>/', ProductDetailApi.as_view(), name='product_detail_api'),
    path('api/descr_points/', DescrPointListApi.as_view(), name='descr_point_list_api'),
    path('api/descr_points/<int:pk>/', DescrPointDetailApi.as_view(), name='descr_point_detail_api'),
    path('api/add_info_points/', AddInfoPointListApi.as_view(), name='add_info_point_list_api'),
    path('api/add_info_points/<int:pk>/', AddInfoPointDetailApi.as_view(), name='add_info_point_detail_api'),
]
