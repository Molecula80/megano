from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    telephone = models.CharField(max_length=255, unique=True, verbose_name='телефон')
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='images/avatars/', verbose_name='аватар')
    is_staff = models.BooleanField(default=False, verbose_name='персонал')
    is_active = models.BooleanField(default=True, verbose_name='активный')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email
