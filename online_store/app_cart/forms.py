from django import forms


class CartAddProductForm(forms.Form):
    """ Форма для добавления товара в корзину. """
    quantity = forms.IntegerField(min_value=0,
                                  widget=forms.TextInput(attrs={"class": "Amount-input form-input", "name": "amount",
                                                                "type": "text", "value": "1"}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
