from django import forms
from django.db.models import Min, Max

from .models import Product


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
    # Рассчитываем минимальную и максимальную цены товаров.
    price_data = Product.objects.prefetch_related('categories').filter(active=True).aggregate(min_price=Min('price'),
                                                                                              max_price=Max('price'))
    price_range = forms.CharField(widget=forms.TextInput(
        attrs={"class": "range-line", "id": "price", "name": "price", "type": "text", "data-type": "double",
               "data-min": price_data['min_price'], "data-max": price_data['max_price']}))
    title = forms.CharField()

    class Meta:
        fields = ('price_range', 'title')
