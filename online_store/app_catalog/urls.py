from django.urls import path

from .views import IndexView, ProductListView, product_detail_view
from .api import CategoryListApi, CategoryDetailApi, FabricatorListApi, FabricatorDetailApi, ProductListApi, \
    ProductDetailApi, DescrPointListApi, DescrPointDetailApi, AddInfoPointListApi, AddInfoPointDetailApi, \
    SellerListApi, SellerDetailApi, ReviewListApi, ReviewDetailApi

app_name = 'app_catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('catalog/delivery/<str:free_delivery>/', ProductListView.as_view(), name='free_delivery'),
    path('catalog/categories/<slug:category_slug>/', ProductListView.as_view(), name='category'),
    path('catalog/sort_order/<str:sort_order>/', ProductListView.as_view(), name='sorted_catalog'),
    path('catalog/products/<slug>/', product_detail_view, name='product_detail'),
    # API
    path('api/categories/', CategoryListApi.as_view(), name='category_list_api'),
    path('api/categories/<int:pk>/', CategoryDetailApi.as_view(), name='category_detail_api'),
    path('api/sellers/', SellerListApi.as_view(), name='seller_list_api'),
    path('api/sellers/<int:pk>/', SellerDetailApi.as_view(), name='seller_detail_api'),
    path('api/fabricators/', FabricatorListApi.as_view(), name='fabricator_list_api'),
    path('api/fabricators/<int:pk>/', FabricatorDetailApi.as_view(), name='fabricator_detail_api'),
    path('api/products/', ProductListApi.as_view(), name='product_list_api'),
    path('api/products/<int:pk>/', ProductDetailApi.as_view(), name='product_detail_api'),
    path('api/descr_points/', DescrPointListApi.as_view(), name='descr_point_list_api'),
    path('api/descr_points/<int:pk>/', DescrPointDetailApi.as_view(), name='descr_point_detail_api'),
    path('api/add_info_points/', AddInfoPointListApi.as_view(), name='add_info_point_list_api'),
    path('api/add_info_points/<int:pk>/', AddInfoPointDetailApi.as_view(), name='add_info_point_detail_api'),
    path('api/reviews/', ReviewListApi.as_view(), name='review_list_api'),
    path('api/reviews/<int:pk>/', ReviewDetailApi.as_view(), name='review_detail_api'),
]
