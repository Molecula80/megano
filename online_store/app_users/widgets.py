from typing import Any
from django import forms


class PhoneWidget(forms.MultiWidget):
    def __init__(self, code_length: int = 3, num_length: int = 7, attrs: Any = None) -> None:
        widgets = [forms.TextInput(attrs={'size': code_length, 'maxlength': code_length}),
                   forms.TextInput(attrs={'size': num_length, 'maxlength': num_length})]
        super(PhoneWidget, self).__init__(widgets, attrs)

    def decompress(self, value) -> list:
        if value:
            return [value.code, value.number]
        else:
            return ['', '']

    @classmethod
    def format_output(cls, rendered_widgets: list) -> str:
        code = rendered_widgets[0]
        number = rendered_widgets[1]
        return '+7({code}){number}'.format(code=code, number=number)
