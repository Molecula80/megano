from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from .models import CartItem
from .serializers import CartItemSerializer
from .filters import CartItemFilter
from common.api import ModelListApi, ModelDetailApi


class CartItemListApi(ModelListApi):
    """ Представление для получения списка единиц корзины и создания новой единицы корзины. """
    permission_required = ('app_cart.view_cart_item', 'app_catalog.add_cart_item')
    queryset = CartItem.objects.select_related('user', 'product').all()
    serializer_class = CartItemSerializer
    filterset_class = CartItemFilter


class CartItemDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о единице корзины, а также её редактирования и удаления. """
    permission_required = ('app_cart.view_cart_item', 'app_cart.change_cart_item', 'app_cart.delete_cart_item')
    queryset = CartItem.objects.select_related('user', 'product').all()
    serializer_class = CartItemSerializer
