from .models import Category, Fabricator, Product, DescrPoint, AddInfoPoint
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для категорий товаров. """
    class Meta:
        model = Category
        fields = '__all__'


class FabricatorSerializer(serializers.ModelSerializer):
    """ Сериализатор для производителей. """
    class Meta:
        model = Fabricator
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор для товаров. """
    class Meta:
        model = Product
        fields = '__all__'


class DescrPointSerializer(serializers.ModelSerializer):
    """ Сериализатор для пунктов описания товара. """
    class Meta:
        model = DescrPoint
        fields = '__all__'


class AddInfoPointSerializer(serializers.ModelSerializer):
    """ Сериализатор для пунктов дополнительной информации о товаре. """
    class Meta:
        model = AddInfoPoint
        fields = '__all__'
