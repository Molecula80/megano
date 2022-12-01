# from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView


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
