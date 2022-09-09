# from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView


class MainPageView(TemplateView):
    """ Главная страница. """
    def get_context_data(self, **kwargs):
        pass


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
