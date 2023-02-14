from .models import Order, OrderItem, DeliveryMethod
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    """ Сериализатор для заказов. """
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    """ Сериализатор для единиц заказов. """
    class Meta:
        model = OrderItem
        fields = '__all__'


class DeliveryMethodSerializer(serializers.ModelSerializer):
    """ Сериализатор для способов доставки. """
    class Meta:
        model = DeliveryMethod
        fields = '__all__'
