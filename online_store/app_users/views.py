from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import RegisterForm
from .models import User


class AccountDetailView(DetailView):
    """ Персональный аккаунт. """
    def get_context_data(self, **kwargs):
        pass


def register_view(request):
    """ Страница регистрации. """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Создаем профиль пользователя.
            second_name = form.cleaned_data.get('second_name')
            telephone = form.cleaned_data.get('telephone')
            avatar = form.cleaned_data.get('avatar')
            Profile.objects.create(user=user, second_name=second_name, telephone=telephone, avatar=avatar)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()
    return render(request, 'app_users/register.html', {'form': form})


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
    next_page = '/'


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

