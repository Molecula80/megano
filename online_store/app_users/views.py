# from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.views import View
from django.views.generic import DetailView, ListView


class AccountDetailView(DetailView):
    """ Персональный аккаунт. """
    def get_context_data(self, **kwargs):
        pass


def register_view(request):
    """ Страница регистрации. """
    pass


def login_view(request):
    """ Страница входа. """
    pass


class ProfileView(View):
    """ Профиль пользователя. """
    def get(self, request, profile_id):
        pass

    def post(self, request, profile_id):
        pass


class UserLogoutView(LogoutView):
    """ Представление для выхода из под учетной записи. """
    pass


class OrderHistoryListView(ListView):
    """ История заказов пользователя. """
    def get_context_data(self, **kwargs):
        pass


class OrderDetailView(DetailView):
    """ Детальная страница заказа. """
    def get_context_data(self, **kwargs):
        pass

    def post(self, request, profile_id, order_id):
        pass

