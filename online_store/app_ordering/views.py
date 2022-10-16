from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import OrderCreateForm, PaymentForm


class OrderCreateView(View):
    """ Ввод параметров пользователя. """
    def get(self, request):
        form = OrderCreateForm()
        return render(request, 'app_ordering/order_create.html', {'form': form, 'page_title': 'Оформление заказа'})

    def post(self, request):
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('app_ordering:payment'))


class PaymentView(View):
    """ Оплата заказа. """
    def get(self, request):
        form = PaymentForm()
        return render(request, 'app_ordering/payment.html', {'form Payment': form, 'page_title': 'Оплата'})

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('app_ordering:progress_payment'))


def progress_payment(request):
    return render(request, 'app_ordering/progress_payment.html', {'page_title': 'Ожидание оплаты'})
