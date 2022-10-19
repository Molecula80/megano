from .models import Category, Fabricator, Product, DescrPoint, AddInfoPoint
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FabricatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricator
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class DescrPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescrPoint
        fields = '__all__'


class AddInfoPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddInfoPoint
        fields = '__all__'
