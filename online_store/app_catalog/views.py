# from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, ListView, DetailView

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from .models import Category
from .serializers import CategorySerializer
from .filters import CategoryFilter


class IndexView(TemplateView):
    """ Главная страница. """
    template_name = 'app_catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductListView(ListView):
    """ Страница со списком товаров. """
    template_name = 'app_catalog/catalog.html'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Каталог'
        return context


class ProductDetailView(DetailView):
    """ Детальная страница товара. """
    template_name = 'app_catalog/product_detail.html'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Продукт'
        return context

    def post(self, request, slug):
        pass


class CategoryListApi(ListModelMixin, CreateModelMixin, GenericAPIView):
    """ Представление для получения списка категорий и создания новой категории. """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter

    def get(self, request):
        return self.list(request)

    def post(self, request, format=None):
        if not request.user.has_perm('app_catalog.add_category'):
            raise PermissionDenied()
        return self.create(request)


class CategoryDetailApi(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """ Представление для получения детальной информации о категории, а также ее редактирования и удаления. """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm('app_catalog.change_category'):
            raise PermissionDenied()
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm('app_catalog.delete_category'):
            raise PermissionDenied()
        return self.destroy(request, *args, **kwargs)
