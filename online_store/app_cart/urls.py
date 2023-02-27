from django.urls import path

from .api import CartItemDetailApi, CartItemListApi
from .views import CartAdd, cart_detail, cart_remove, cart_update

app_name = 'app_cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', CartAdd.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('update/', cart_update, name='cart_update'),
    # API
    path('api/cart_items/', CartItemListApi.as_view(), name='cart_item_list_api'),
    path('api/cart_items/<int:pk>/', CartItemDetailApi.as_view(), name='cart_item_detail_api'),
]
