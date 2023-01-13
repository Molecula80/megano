from django import forms
from .models import DeliveryMethod


class OrderCreateForm(forms.Form):
    """ Форма для оформления заказа. """
    full_name = forms.CharField(max_length=255,
                                error_messages={'required': 'Это поле обязательно для заполнения.'},
                                widget=forms.TextInput(attrs={"class": "form-input", "id": "name", "name": "name",
                                                              "type": "text"}))
    telephone = forms.CharField(max_length=255,
                                error_messages={'required': 'Это поле обязательно для заполнения.',
                                                'invalid': 'Это значение недопустимо.'},
                                widget=forms.TextInput(attrs={"class": "form-input", "id": "phone", "name": "phone",
                                                              "type": "text", "data-mask": "+7(999)999-99-99"}))
    email = forms.EmailField(error_messages={'required': 'Это поле обязательно для заполнения.',
                                             'invalid': 'Это значение недопустимо.'},
                             widget=forms.EmailInput(attrs={"class": "form-input", "id": "mail", "name": "mail",
                                                            "type": "text", "value": "", "data-validate": "require"}))
    delivery_method = forms.ModelChoiceField(queryset=DeliveryMethod.objects.all(), empty_label=None,
                                             widget=forms.RadioSelect(attrs={"id": "delivery-method"}))
    city = forms.CharField(max_length=255, error_messages={'required': 'Это поле обязательно для заполнения.'},
                           widget=forms.TextInput(attrs={"class": "form-input", "id": "city", "name": "city",
                                                         "type": "text"}))
    address = forms.CharField(error_messages={'required': 'Это поле обязательно для заполнения.'},
                              widget=forms.Textarea(attrs={"class": "form-textarea", "name": "address",
                                                           "id": "address"}))
    payment_method = forms.ChoiceField(choices=[(1, 'Онлайн картой'), (2, 'Онлайн со случайного чужого счета')],
                                       widget=forms.RadioSelect(attrs={"id": "payment-method"}))
