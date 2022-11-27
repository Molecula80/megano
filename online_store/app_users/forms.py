from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class AuthForm(forms.Form):
    """ Форма для аутентификации пользователя. """
    email = forms.CharField(label='Имя пользователя',
                            error_messages={'required': 'Это поле обязательно для заполнения.'},
                            widget=forms.EmailInput(attrs={"class": "form-input", "id": "mail", "name": "mail",
                                                           "type": "text", "value": "", "data-validate": "require"}))
    password = forms.CharField(label='Пароль',
                               error_messages={'required': 'Это поле обязательно для заполнения.'},
                               widget=forms.PasswordInput(attrs={"class": "form-input", "id": "password",
                                                                 "name": "password", "type": "password",
                                                                 "placeholder": ""}))


class RegisterForm(UserCreationForm):
    """ Форма регистрации пользователя. """
    full_name = forms.CharField(max_length=255, required=True,
                                error_messages={'required': 'Это поле обязательно для заполнения.'},
                                widget=forms.TextInput(attrs={"class": "form-input", "id": "name", "name": "name",
                                                              "type": "text", "value": "", "data-validate": "require"}))
    telephone = forms.CharField(max_length=255, required=False,
                                error_messages={'invalid': 'Это значение недопустимо.'},
                                widget=forms.TextInput(attrs={"class": "form-input", "id": "phone", "name": "phone",
                                                              "type": "text", "value": "",
                                                              "data-mask": "+7(999)999-99-99"}))
    email = forms.EmailField(required=True, error_messages={'required': 'Это поле обязательно для заполнения.',
                                                            'invalid': 'Это значение недопустимо.',
                                                            'unique': 'Пользователь с таким email уже есть.'},
                             widget=forms.EmailInput(attrs={"class": "form-input", "id": "mail", "name": "mail",
                                                            "type": "text", "value": "", "data-validate": "require"}))
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(attrs={"class": "Profile-file form-input", "id": "avatar",
                                                            "name": "avatar", "type": "file",
                                                            "data-validate": "onlyImgAvatar"}))
    password1 = forms.CharField(error_messages={'required': 'Это поле обязательно для заполнения.'},
                                widget=forms.PasswordInput(attrs={"class": "form-input", "id": "password",
                                                                  "name": "password", "type": "password",
                                                                  "placeholder": ""}))
    password2 = forms.CharField(error_messages={'required': 'Это поле обязательно для заполнения.'},
                                widget=forms.PasswordInput(attrs={"class": "form-input", "id": "passwordReply",
                                                                  "name": "passwordReply", "type": "password",
                                                                  "placeholder": "Введите пароль повторно"}))

    class Meta:
        model = User
        fields = ('full_name', 'telephone', 'email', 'avatar', 'password1', 'password2')
