from django.core.exceptions import PermissionDenied

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from .serializers import CategorySerializer, FabricatorSerializer, ProductSerializer, DescrPointSerializer, \
    AddInfoPointSerializer
from .filters import CategoryFilter, ProductFilter

from .models import Category, Fabricator, Product, DescrPoint, AddInfoPoint


class ModelListApi(ListModelMixin, CreateModelMixin, GenericAPIView):
    """ Представление для получения списка моделей и создания новой модели. """
    model_name = str()

    def get(self, request) -> list:
        """
        Метод для получения списка моделей.
        :param request:
        :return: список моделей
        :rtype: list
        """
        return self.list(request)

    def post(self, request, format=None):
        """ Метод для создания новой модели. """
        if not request.user.has_perm('app_catalog.add_{}'.format(self.model_name)):
            raise PermissionDenied()
        return self.create(request)


class ModelDetailApi(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """ Представление для получения детальной информации о модели, а также ее редактирования и удаления. """
    model_name = str()

    def get(self, request, *args, **kwargs):
        """ Метод для получения детальной информации о модели. """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """ Метод для редактирования модели. """
        if not request.user.has_perm('app_catalog.change_{}'.format(self.model_name)):
            raise PermissionDenied()
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """ Метод для удаления модели. """
        if not request.user.has_perm('app_catalog.delete_{}'.format(self.model_name)):
            raise PermissionDenied()
        return self.destroy(request, *args, **kwargs)


class CategoryListApi(ModelListApi):
    """ Представление для получения списка категорий и создания новой категории. """
    queryset = Category.objects.select_related('parent').all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    model_name = 'category'


class CategoryDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о категории, а также ее редактирования и удаления. """
    queryset = Category.objects.select_related('parent').all()
    serializer_class = CategorySerializer
    model_name = 'category'


class FabricatorListApi(ModelListApi):
    """ Представление для получения списка производителей и создания нового производителя. """
    queryset = Fabricator.objects.all()
    serializer_class = FabricatorSerializer
    filterset_fields = ['title']
    model_name = 'fabricator'


class FabricatorDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о производителе, а также его редактирования и удаления. """
    queryset = Fabricator.objects.all()
    serializer_class = FabricatorSerializer
    model_name = 'fabricator'


class ProductListApi(ModelListApi):
    """ Представление для получения списка товаров и создания нового товара. """
    queryset = Product.objects.select_related('fabricator').prefetch_related('categories').all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    model_name = 'product'


class ProductDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о товаре, а также его редактирования и удаления. """
    queryset = Product.objects.select_related('fabricator').prefetch_related('categories').all()
    serializer_class = ProductSerializer
    model_name = 'product'


class DescrPointListApi(ModelListApi):
    """ Представление для получения списка пунктов описания и создания нового пункта описания. """
    queryset = DescrPoint.objects.select_related('product').all()
    serializer_class = DescrPointSerializer
    filterset_fields = ['product', 'content']
    model_name = 'descr_point'


class DescrPointDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о пункте описания, а также его редактирования и удаления. """
    queryset = DescrPoint.objects.select_related('product').all()
    serializer_class = DescrPointSerializer
    model_name = 'descr_point'


class AddInfoPointListApi(ModelListApi):
    """ Представление для получения списка пункта доп. информации и создания нового пункта. """
    queryset = AddInfoPoint.objects.select_related('product').all()
    serializer_class = AddInfoPointSerializer
    filterset_fields = ['product', 'characteristic', 'value']
    model_name = 'add_info_point'


class AddInfoPointDetailApi(ModelDetailApi):
    """
    Представление для получения детальной информации о пункте доп. информации, а также его редактирования и удаления.
    """
    queryset = AddInfoPoint.objects.select_related('product').all()
    serializer_class = AddInfoPointSerializer
    model_name = 'add_info_point'
