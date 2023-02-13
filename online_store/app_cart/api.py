from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from .models import CartItem
from .serializers import CartItemSerializer
from .filters import CartItemFilter


class CartItemListApi(PermissionRequiredMixin, ListModelMixin, CreateModelMixin, GenericAPIView):
    """ Представление для получения списка единиц корзины и создания новой единицы корзины. """
    permission_required = ('app_cart.view_cart_item', 'app_catalog.add_cart_item')
    queryset = CartItem.objects.select_related('user', 'product').all()
    serializer_class = CartItemSerializer
    filterset_class = CartItemFilter

    def get(self, request) -> list:
        """
        Метод для получения списка единиц корзины.
        :param request:
        :return: список единиц корзины
        :rtype: list
        """
        return self.list(request)

    def post(self, request, format=None):
        """ Метод для создания новой единицы корзины. """
        return self.create(request)


class CartItemDetailApi(PermissionRequiredMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """ Представление для получения детальной информации о единице корзины, а также её редактирования и удаления. """
    permission_required = ('app_cart.view_cart_item', 'app_cart.change_cart_item', 'app_cart.delete_cart_item')
    queryset = CartItem.objects.select_related('user', 'product').all()
    serializer_class = CartItemSerializer

    def get(self, request, *args, **kwargs):
        """ Метод для получения детальной информации о единице корзины. """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """ Метод для редактирования единицы корзины. """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """ Метод для удаления единицы корзины. """
        return self.destroy(request, *args, **kwargs)
