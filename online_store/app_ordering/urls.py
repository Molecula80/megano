from django.urls import path

from .api import (DeliveryMethodDetailApi, DeliveryMethodListApi,
                  OrderDetailApi, OrderItemDetailApi, OrderItemListApi,
                  OrderListApi)
from .views import (OrderCreateView, PaymentView, get_delivery_method,
                    progress_payment, register_view)

app_name = 'app_ordering'

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order_create'),
    path('register/', register_view, name='register'),
    path('payment/<int:order_id>/', PaymentView.as_view(), name='payment'),
    path('payment/<int:order_id>/<str:someone>/', PaymentView.as_view(), name='payment_someone'),
    path('progress_payment/<int:order_id>/', progress_payment, name='progress_payment'),
    path('get_delivery_method/', get_delivery_method, name='get_delivery_method'),
    # API
    path('api/orders/', OrderListApi.as_view(), name='order_list_api'),
    path('api/orders/<int:pk>/', OrderDetailApi.as_view(), name='order_detail_api'),
    path('api/order_items/', OrderItemListApi.as_view(), name='order_item_list_api'),
    path('api/order_items/<int:pk>/', OrderItemDetailApi.as_view(), name='order_item_detail_api'),
    path('api/delivery_methods/', DeliveryMethodListApi.as_view(), name='delivery_method_list_api'),
    path('api/delivery_methods/<int:pk>/', DeliveryMethodDetailApi.as_view(), name='delivery_method_detail_api'),
]
