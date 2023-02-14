from .models import Order, OrderItem, DeliveryMethod
from .serializers import OrderSerializer, OrderItemSerializer, DeliveryMethodSerializer
from .filters import OrderFilter, OrderItemFilter
from common.api import ModelListApi, ModelDetailApi


class OrderListApi(ModelListApi):
    """ Представление для получения списка заказов и создания нового заказа. """
    permission_required = ('app_ordering.view_order', 'app_ordering.add_order')
    queryset = Order.objects.select_related('user', 'delivery_method').all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter


class OrderDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о заказе, а также его редактирования и удаления. """
    permission_required = ('app_ordering.view_order', 'app_ordering.change_order', 'app_ordering.delete_order')
    queryset = Order.objects.select_related('user', 'delivery_method').all()
    serializer_class = OrderSerializer


class OrderItemListApi(ModelListApi):
    """ Представление для получения списка единиц заказов и создания новой единицы заказа. """
    permission_required = ('app_ordering.view_order_item', 'app_ordering.add_order_item')
    queryset = OrderItem.objects.select_related('order', 'product').all()
    serializer_class = OrderItemSerializer
    filterset_class = OrderItemFilter


class OrderItemDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о единице заказа, а также её редактирования и удаления. """
    permission_required = ('app_ordering.view_order', 'app_ordering.change_order', 'app_ordering.delete_order')
    queryset = OrderItem.objects.select_related('order', 'product').all()
    serializer_class = OrderItemSerializer


class DeliveryMethodListApi(ModelListApi):
    """ Представление для получения списка способов доставки и создания нового способа доставки. """
    permission_required = ('app_ordering.view_delivery_method', 'app_ordering.add_delivery_method')
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer


class DeliveryMethodDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о способе доставки, а также его редактирования и удаления. """
    permission_required = ('app_ordering.view_delivery_method', 'app_ordering.change_delivery_method',
                           'app_ordering.delete_delivery_method')
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer
