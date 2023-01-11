import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .forms import AuthForm, ProfileForm, RegisterForm
from .models import User
from app_cart.cart import Cart
from app_cart.models import CartItem
from common.functions import register


logger = logging.getLogger(__name__)


class AccountDetailView(LoginRequiredMixin, DetailView):
    """ Персональный аккаунт. """
    model = User
    template_name = 'app_users/account_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        if self.object != self.request.user:
            raise Http404
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Личный кабинет'
        context['section'] = 'account'
        logger.debug('Пользователь {} запросил страницу личного кабинета.'.format(self.request.user.email))
        return context


def register_view(request):
    """ Страница регистрации. """
    next_page = 'app_catalog:index'
    template = 'app_users/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        context = {'form': form, 'page_title': 'регистрация'}
        if form.is_valid():
            return register(request=request, next_page=next_page, form=form, template=template, context=context)
    else:
        form = RegisterForm()
    return render(request, template, {'form': form, 'page_title': 'регистрация'})


def login_view(request):
    """ Страница входа. """
    error = str()
    cart = Cart(request)
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    auth_cart = CartItem.objects.filter(user=user)
                    cart.merge_carts(auth_cart)
                    cart.delete_cart_from_database(auth_cart)
                    logger.debug('Пользователь {} вошел в систему.'.format(email))
                    return HttpResponseRedirect(reverse('app_catalog:index'))
                else:
                    error = 'Ошибка! Аккаунт пользователя неактивен.'
            else:
                error = 'Ошибка! Проверьте правильность написания email и пароля.'
    else:
        form = AuthForm()
    context = {
        'form': form,
        'page_title': 'авторизация',
        'error': error
    }
    return render(request, 'app_users/login.html', context=context)


@login_required
def profile_view(request, pk):
    """ Страница изменения профиля пользователя. """
    page_title = 'профиль'
    section = 'profile'
    success = False
    user = get_object_or_404(User, id=pk)
    if user != request.user:
        raise Http404
    old_number = str(user.telephone)  # Старый номер телефона.
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            telephone_str = form.cleaned_data.get('telephone')
            # Оставляем все цифры, кроме семёрки.
            telephone = ''.join(sym for sym in telephone_str[3:] if sym.isdigit())
            if telephone and len(telephone) < 10:
                form.add_error('telephone', 'Это значение недопустимо.')
            # Если был введен номер телефона, и пользователь с указанным номером телефона уже есть,
            # выводим сообщение об ошибке.
            # Если пользователь не поменял свой номер телефона, сообщение об ошибке не выводится.
            elif telephone and telephone != old_number and \
                    User.objects.only('telephone').filter(telephone=telephone).exists():
                form.add_error('telephone', 'Пользователь с таким номером телефона уже есть.')
            else:
                user.telephone = telephone
                user.set_password(form.cleaned_data['password1'])
                user.save()
                cart = Cart(request)
                cart.save_cart_in_database(user=user)
                success = True
                logger.debug('Пользователь {email} изменил свой профиль.\nОбновленные данные:'
                             '\nФИО: {name}\nТелефон: {telephone}\nEmail: {email}'.format(email=user.email,
                                                                                          name=user.full_name,
                                                                                          telephone=user.telephone))
    else:
        form = ProfileForm(instance=user)
        logger.debug('Пользователь {email} запросил страницу профиля.\nДанные пользователя:'
                     '\nФИО: {name}\nТелефон: {telephone}\nEmail: {email}'.format(email=user.email,
                                                                                  name=user.full_name,
                                                                                  telephone=user.telephone))
    return render(request, 'app_users/edit_profile.html', {'form': form, 'page_title': page_title, 'section': section,
                                                           'success': success})


def logout_view(request):
    """ Представление для выхода из под учетной записи. """
    cart = Cart(request)
    cart.save_cart_in_database(user=request.user)
    logout(request)
    return HttpResponseRedirect(reverse('app_catalog:index'))


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
