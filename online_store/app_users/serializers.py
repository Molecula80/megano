from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для пользователей. """
    class Meta:
        model = User
        fields = ['id', 'password', 'last_login', 'is_superuser', 'full_name', 'telephone', 'email', 'is_staff',
                  'is_active', 'date_joined', 'groups']
