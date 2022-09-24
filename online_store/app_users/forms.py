from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    """ Форма регистрации пользователя. """
    full_name = forms.CharField(max_length=255, required=True)
    telephone = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('full_name', 'telephone', 'email', 'avatar', 'password1', 'password2')
