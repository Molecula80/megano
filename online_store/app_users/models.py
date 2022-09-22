from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, verbose_name='имя пользователя')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    telephone = models.CharField(max_length=30, blank=True, unique=True, verbose_name='телефон')
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='images/avatars/', blank=True, null=True, verbose_name='иконка')
    active = models.BooleanField(default=True, verbose_name='активен')
    groups = models.ManyToManyField(Group, verbose_name='группы')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
