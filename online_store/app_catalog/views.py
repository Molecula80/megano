# from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from .models import Category
from .serializers import CategorySerializer


class IndexView(TemplateView):
    """ Главная страница. """
    template_name = 'app_catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductListView(ListView):
    """ Страница со списком товаров. """
    def get_context_data(self, **kwargs):
        pass


class ProductDetailView(DetailView):
    """ Детальная страница товара. """
    def get_context_data(self, **kwargs):
        pass

    def post(self, request, slug):
        pass


class CategoryList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        return self.list(request)

    def post(self, request, format=None):
        return self.create(request)
