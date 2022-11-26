from django import forms

from .widgets import PhoneWidget


class PhoneField(forms.MultiValueField):
    def __init__(self, code_length: int = 3, num_length: int = 7, *args, **kwargs) -> None:
        list_fields = [forms.CharField, forms.CharField]
        super(PhoneField, self).__init__(list_fields, widget=PhoneWidget(code_length, num_length), *args, **kwargs)

    def compress(self, values: list) -> str:
        code = values[0]
        number = values[1]
        return '+7({code}){number}'.format(code=code, number=number)

