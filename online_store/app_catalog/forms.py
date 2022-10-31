from django import forms


class ReviewForm(forms.Form):
    """ Форма для добавления отзыва к товару. """
    text = forms.CharField(widget=forms.TextInput(attrs={"class": "form-textarea", "name": "review", "id": "review",
                                                         "placeholder": "Отзыв"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input", "id": "name", "name": "name",
                                                         "type": "text", "placeholder": "Имя"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-input", "id": "email", "name": "email",
                                                            "type": "text", "placeholder": "Email"}))

    class Meta:
        fields = ('text', 'name', 'email')


class ProductFilterForm(forms.Form):
    """ Форма для фильтрацции товаров в каталоге. """
    min_price = forms.IntegerField(min_value=0)
    max_price = forms.IntegerField(min_value=0)
    price_range = forms.MultiValueField(fields=[min_price, max_price],
                                        widget={"class": "range-line", "id": "price", "name": "price", "type": "text",
                                                "data-type": "double", "data-min": "7", "data-max": "50",
                                                "data-from": "7", "data-to": "27"})

    class Meta:
        fields = ('price_range',)
