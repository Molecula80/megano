from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """ Сериализатор для единиц корзины. """
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'quantity']
