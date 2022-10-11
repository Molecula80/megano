from django.urls import path

from .views import IndexView, CategoryListApi, CategoryDetailApi

app_name = 'app_catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/categories/', CategoryListApi.as_view(), name='category_list_api'),
    path('api/categories/<int:pk>/', CategoryDetailApi.as_view(), name='category_detail_api'),
]
