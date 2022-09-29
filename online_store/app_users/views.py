from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import RegisterForm, AuthForm


class AccountDetailView(DetailView):
    """ Персональный аккаунт. """
    def get_context_data(self, **kwargs):
        pass


def register_view(request):
    """ Страница регистрации. """
    page_title = 'регистрация'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
    else:
        form = RegisterForm()
    return render(request, 'app_users/register.html', {'form': form, 'page_title': page_title})


def login_view(request):
    """ Страница входа. """
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            email = auth_form.cleaned_data['email']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Вы успешно вошли.')
                else:
                    auth_form.add_error('__all__', 'Ошибка! Аккаунт пользователя неактивен.')
            else:
                auth_form.add_error('__all__', 'Ошибка! Проверьте написание имя пользователя и пароля.')
    else:
        auth_form = AuthForm()

    context = {
        'form': auth_form,
        'page_title': 'авторизация'
    }
    return render(request, 'app_users/login.html', context=context)


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

