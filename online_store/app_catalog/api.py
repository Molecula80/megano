from common.api import ModelDetailApi, ModelListApi

from .filters import CategoryFilter, ProductFilter
from .models import (AddInfoPoint, Category, DescrPoint, Fabricator, Product,
                     Review, Seller)
from .serializers import (AddInfoPointSerializer, CategorySerializer,
                          DescrPointSerializer, FabricatorSerializer,
                          ProductSerializer, ReviewSerializer,
                          SellerSerializer)


class CategoryListApi(ModelListApi):
    """ Представление для получения списка категорий и создания новой категории. """
    permission_required = ('app_catalog.view_category', 'app_catalog.add_category')
    queryset = Category.objects.select_related('parent').all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter


class CategoryDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о категории, а также ее редактирования и удаления. """
    permission_required = ('app_catalog.view_category', 'app_catalog.change_category', 'app_catalog.delete_category')
    queryset = Category.objects.select_related('parent').all()
    serializer_class = CategorySerializer


class SellerListApi(ModelListApi):
    """ Представление для получения списка продавцов и создания нового продавца. """
    permission_required = ('app_catalog.view_seller', 'app_catalog.add_seller')
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    filterset_fields = ['name']


class SellerDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о продавце, а также его редактирования и удаления. """
    permission_required = ('app_catalog.view_seller', 'app_catalog.change_seller', 'app_catalog.delete_seller')
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class FabricatorListApi(ModelListApi):
    """ Представление для получения списка производителей и создания нового производителя. """
    permission_required = ('app_catalog.view_fabricator', 'app_catalog.add_fabricator')
    queryset = Fabricator.objects.all()
    serializer_class = FabricatorSerializer
    filterset_fields = ['title']


class FabricatorDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о производителе, а также его редактирования и удаления. """
    permission_required = ('app_catalog.view_fabricator', 'app_catalog.change_fabricator',
                           'app_catalog.delete_fabricator')
    queryset = Fabricator.objects.all()
    serializer_class = FabricatorSerializer


class ProductListApi(ModelListApi):
    """ Представление для получения списка товаров и создания нового товара. """
    permission_required = ('app_catalog.view_product', 'app_catalog.add_product')
    queryset = Product.objects.select_related('fabricator').prefetch_related('categories').all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter


class ProductDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о товаре, а также его редактирования и удаления. """
    permission_required = ('app_catalog.view_product', 'app_catalog.change_product', 'app_catalog.delete_product')
    queryset = Product.objects.select_related('fabricator').prefetch_related('categories').all()
    serializer_class = ProductSerializer


class DescrPointListApi(ModelListApi):
    """ Представление для получения списка пунктов описания и создания нового пункта описания. """
    permission_required = ('app_catalog.view_descr_point', 'app_catalog.add_descr_point')
    queryset = DescrPoint.objects.select_related('product').all()
    serializer_class = DescrPointSerializer
    filterset_fields = ['product', 'content']


class DescrPointDetailApi(ModelDetailApi):
    """ Представление для получения детальной информации о пункте описания, а также его редактирования и удаления. """
    permission_required = ('app_catalog.view_descr_point', 'app_catalog.change_descr_point',
                           'app_catalog.delete_descr_point')
    queryset = DescrPoint.objects.select_related('product').all()
    serializer_class = DescrPointSerializer


class AddInfoPointListApi(ModelListApi):
    """ Представление для получения списка пунктов доп. информации и создания нового пункта. """
    permission_required = ('app_catalog.view_add_info_point', 'app_catalog.add_add_info_point')
    queryset = AddInfoPoint.objects.select_related('product').all()
    serializer_class = AddInfoPointSerializer
    filterset_fields = ['product', 'characteristic', 'value']


class AddInfoPointDetailApi(ModelDetailApi):
    """
    Представление для получения детальной информации о пункте доп. информации, а также его редактирования и удаления.
    """
    permission_required = ('app_catalog.view_add_info_point', 'app_catalog.change_add_info_point',
                           'app_catalog.delete_add_info_point')
    queryset = AddInfoPoint.objects.select_related('product').all()
    serializer_class = AddInfoPointSerializer


class ReviewListApi(ModelListApi):
    """ Представление для получения списка отзывов о товарах и создания нового отзыва. """
    permission_required = ('app_catalog.view_review', 'app_catalog.add_review')
    queryset = Review.objects.select_related('product', 'user').all()
    serializer_class = ReviewSerializer
    filterset_fields = ['product', 'user', 'name', 'email', 'active']


class ReviewDetailApi(ModelDetailApi):
    """
    Представление для получения детальной информации об отзыве о товаре, а также его редактирования и удаления.
    """
    permission_required = ('app_catalog.view_review', 'app_catalog.change_review', 'app_catalog.delete_review')
    queryset = Review.objects.select_related('product', 'user').all()
    serializer_class = ReviewSerializer
