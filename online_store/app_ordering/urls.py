from django.urls import path

from .views import OrderCreateView, PaymentView, progress_payment

app_name = 'app_ordering'

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order_create'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('progress_payment/', progress_payment, name='progress_payment'),
]
