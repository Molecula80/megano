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
    price_range = forms.CharField(widget=forms.TextInput(attrs={"class": "range-line", "id": "price", "name": "price",
                                                                "type": "text", "data-type": "double", "data-min": "0",
                                                                "data-max": "1000", "data-from": "0",
                                                                "data-to": "500"}))

    class Meta:
        fields = ('price_range',)
