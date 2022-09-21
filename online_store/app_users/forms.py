from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AuthForm(forms.Form):
    """ Форма аутентификации пользователя. """
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class RegisterForm(UserCreationForm):
    """ Форма регистрации пользователя. """
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    second_name = forms.CharField(max_length=30, required=False, label='Отчество')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    email_address = forms.EmailField(required=True, label='Email')
    telephone = forms.CharField(max_length=30, required=False, label='Телефон')
    avatar = forms.ImageField(required=False, label='аватар')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'second_name', 'last_name', 'email_address', 'telephone', 'avatar',
                  'password1', 'password2')
