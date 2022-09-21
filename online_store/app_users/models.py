from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='пользователь')
    second_name = models.CharField(max_length=30, blank=True, verbose_name='отчество')
    telephone = models.CharField(max_length=30, blank=True, unique=True, verbose_name='телефон')
    avatar = models.ImageField(upload_to='images/avatars/', blank=True, null=True, verbose_name='иконка')

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return '{}'.format(self.user)
