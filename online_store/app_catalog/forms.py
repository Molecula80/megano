from django import forms
from django.db.models import Min, Max

from .models import Product, Seller, Fabricator, Review


class ReviewForm(forms.ModelForm):
    """ Форма для добавления отзыва к товару. """
    text = forms.CharField(error_messages={'required': 'Это поле обязательно для заполнения.'},
                           widget=forms.Textarea(attrs={"class": "form-textarea", "name": "review", "id": "review",
                                                        "placeholder": "Отзыв"}))
    name = forms.CharField(error_messages={'required': 'Это поле обязательно для заполнения.'},
                           widget=forms.TextInput(attrs={"class": "form-input", "id": "name", "name": "name",
                                                         "type": "text", "placeholder": "Имя"}))
    email = forms.EmailField(error_messages={'required': 'Это поле обязательно для заполнения.',
                                             'invalid': 'Это значение недопустимо.'},
                             widget=forms.EmailInput(attrs={"class": "form-input", "id": "email", "name": "email",
                                                            "type": "text", "placeholder": "Email"}))

    class Meta:
        model = Review
        fields = ('text', 'name', 'email')


class ProductFilterForm(forms.Form):
    """ Форма для фильтрацции товаров в каталоге. """
    # Рассчитываем минимальную и максимальную цены товаров.
    price_data = Product.objects.prefetch_related('categories').filter(active=True).aggregate(min_price=Min('price'),
                                                                                              max_price=Max('price'))
    price_range = forms.CharField(widget=forms.TextInput(
        attrs={"class": "range-line", "id": "price", "name": "price", "type": "text", "data-type": "double",
               "data-min": price_data['min_price'], "data-max": price_data['max_price']}))
    title = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"class": "form-input form-input_full", "id": "title", "name": "title", "type": "text",
               "placeholder": "Название"}))
    sellers = forms.ModelMultipleChoiceField(queryset=Seller.objects.all().order_by('name'), required=False,
                                             widget=forms.CheckboxSelectMultiple)
    fabricators = forms.ModelMultipleChoiceField(queryset=Fabricator.objects.all().order_by('title'), required=False,
                                                 widget=forms.CheckboxSelectMultiple)
    in_stock = forms.NullBooleanField(required=False,
                                      widget=forms.Select(choices=[('', 'Не применять'), (True, 'Да'), (False, 'Нет')]))
    free_delivery = forms.NullBooleanField(required=False, widget=forms.Select(
        choices=[('', 'Не применять'), (True, 'Да'), (False, 'Нет')]))

    class Meta:
        fields = ('price_range', 'title', 'sellers', 'fabricators', 'in_stock', 'free_delivery')
