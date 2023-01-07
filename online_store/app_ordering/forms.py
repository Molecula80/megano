from django import forms


class OrderCreateForm(forms.Form):
    """ Форма для оформления заказа. """
    full_name = forms.CharField(max_length=255, required=True,
                                error_messages={'required': 'Это поле обязательно для заполнения.'},
                                widget=forms.TextInput(attrs={"class": "form-input", "id": "name", "name": "name",
                                                              "type": "text"}))
    telephone = forms.CharField(max_length=255, required=False,
                                widget=forms.TextInput(attrs={"class": "form-input", "id": "phone", "name": "phone",
                                                              "type": "text", "data-mask": "+7(999)999-99-99"}))
    email = forms.EmailField(required=True, error_messages={'required': 'Это поле обязательно для заполнения.',
                                                            'invalid': 'Это значение недопустимо.',
                                                            'unique': 'Пользователь с указанным email уже существует.'},
                             widget=forms.EmailInput(attrs={"class": "form-input", "id": "mail", "name": "mail",
                                                            "type": "text", "value": "", "data-validate": "require"}))
