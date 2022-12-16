from django.urls import path

from .views import cart_detail, cart_remove, cart_update, CartAdd

app_name = 'app_cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', CartAdd.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('update/', cart_update, name='cart_update'),
]
