import logging

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

from app_users.models import User


logger = logging.getLogger(__name__)


def register(request, next_page: str, form):
    """ Регистрация пользователя. """
    user = form.save(commit=False)
    telephone_str = form.cleaned_data.get('telephone')
    # Оставляем все цифры, кроме семёрки.
    telephone = ''.join(sym for sym in telephone_str[3:] if sym.isdigit())
    if telephone and len(telephone) < 10:
        form.add_error('telephone', 'Это значение недопустимо.')
    # Если был введен номер телефона, и пользователь с указанным номером телефона уже есть,
    # выводим сообщение об ошибке.
    elif telephone and User.objects.only('telephone').filter(telephone=telephone).exists():
        form.add_error('telephone', 'Пользователь с таким номером телефона уже есть.')
    else:
        user.telephone = telephone
        user.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        login(request, user)
        logger.debug('Пользователь {} зарегистрировался на сайте.'.format(email))
        return HttpResponseRedirect(reverse(next_page))
