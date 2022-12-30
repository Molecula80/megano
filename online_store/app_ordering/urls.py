from django.urls import path

from .views import OrderCreateView, register_view, PaymentView, progress_payment

app_name = 'app_ordering'

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order_create'),
    path('register/', register_view, name='register'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('progress_payment/', progress_payment, name='progress_payment'),
]
