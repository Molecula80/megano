# from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class UserParamsView(View):
    """ Ввод параметров пользователя. """
    def get(self, request):
        pass

    def post(self, request):
        pass


class DeliveryMethodView(View):
    """ Выбор способа доставки. """
    def get(self, request):
        pass

    def post(self, request):
        pass


class PaymentMethodView(View):
    """ Выбор способа оплаты. """
    def get(self, request):
        pass

    def post(self, request):
        pass


class OrderConfirmationView(TemplateView):
    """ Подтверждение заказа. """
    def get_context_data(self, **kwargs):
        pass

    def post(self):
        pass


def payment_process(request):
    """ Оплата заказа. """
    pass
