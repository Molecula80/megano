from django.urls import path

from .views import OrderCreateView, register_view, PaymentView, PaymentSomeoneView, progress_payment, \
    get_delivery_method

app_name = 'app_ordering'

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order_create'),
    path('register/', register_view, name='register'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment_someone/', PaymentSomeoneView.as_view(), name='payment_someone'),
    path('progress_payment/', progress_payment, name='progress_payment'),
    path('get_delivery_method/', get_delivery_method, name='get_delivery_method'),
]
