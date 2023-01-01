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
                                widget=forms.TextInput(attrs={"class": "form-input", "id": "phone", "name": "phone",
                                                              "type": "text", "value": "",
                                                              "data-mask": "+7(999)999-99-99"}))
    email = forms.EmailField(required=True, error_messages={'required': 'Это поле обязательно для заполнения.',
                                                            'invalid': 'Это значение недопустимо.',
                                                            'unique': 'Пользователь с указанным email существует, '
                                                                      'вы можете авторизоваться.'},
                             widget=forms.EmailInput(attrs={"class": "form-input", "id": "mail", "name": "mail",
                                                            "type": "text", "value": "", "data-validate": "require"}))
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(attrs={"class": "Profile-file form-input", "id": "avatar",
                                                            "name": "avatar", "type": "file",
                                                            "data-validate": "onlyImgAvatar"}))
    password1 = forms.CharField(error_messages={'required': 'Это поле обязательно для заполнения.'},
                                widget=forms.PasswordInput(attrs={"class": "form-input", "id": "password",
                                                                  "name": "password", "type": "password"}))
    password2 = forms.CharField(error_messages={'required': 'Это поле обязательно для заполнения.'},
                                widget=forms.PasswordInput(attrs={"class": "form-input", "id": "passwordReply",
                                                                  "name": "passwordReply", "type": "password",
                                                                  "placeholder": "Введите пароль повторно"}))

    class Meta:
        model = User
        fields = ('full_name', 'telephone', 'email', 'avatar', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    """ Форма изменения профиля пользователя. """
    full_name = forms.CharField(max_length=255, required=True,
                                error_messages={'required': 'Это поле обязательно для заполнения.'},
                                widget=forms.TextInput(attrs={"class": "form-input", "id": "name", "name": "name",
                                                              "type": "text", "value": "", "data-validate": "require"}))
    telephone = forms.CharField(max_length=255, required=False,
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
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input", "id": "password",
                                                                  "name": "password", "type": "password",
                                                                  "placeholder": "Тут можно изменить пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input", "id": "passwordReply",
                                                                  "name": "passwordReply", "type": "password",
                                                                  "placeholder": "Введите пароль повторно"}))

    class Meta:
        model = User
        fields = ('full_name', 'telephone', 'email', 'avatar', 'password1', 'password2')

    def clean_password2(self) -> str:
        """ Метод для смены пароля. """
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
