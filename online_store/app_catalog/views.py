# from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView

from .models import Category
from .forms import ReviewForm


class IndexView(TemplateView):
    """ Главная страница. """
    template_name = 'app_catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['three_categories'] = Category.objects.filter(active=True).order_by('-sort_index')[:3]
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
        context['form'] = ReviewForm()
        context['reviews_count'] = 1
        return context

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            return HttpResponse('Отзыв успешно добавлен.')
