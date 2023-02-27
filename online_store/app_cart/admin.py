from django.contrib import admin

from .models import CartItem


class CartItemAdmin(admin.ModelAdmin):
    """ Административная модель товара. """
    list_display = ['id', 'user', 'product', 'quantity']
    list_filter = ['user', 'product']


admin.site.register(CartItem, CartItemAdmin)
