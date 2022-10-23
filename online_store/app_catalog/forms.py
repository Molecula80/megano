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
