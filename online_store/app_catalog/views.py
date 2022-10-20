# from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView

from .models import Category, Product
from .forms import ReviewForm


class IndexView(TemplateView):
    """ Главная страница. """
    template_name = 'app_catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['three_categories'] = Category.objects.filter(active=True).order_by('-sort_index')[:3]
        context['popular_products'] = Product.objects.filter(in_stock=True).order_by('-sort_index')[:8]
        context['limited_edition'] = \
            Product.objects.filter(in_stock=True, limited_edition=True).order_by('-sort_index')[:16]
        return context


class ProductListView(ListView):
    """ Страница со списком товаров. """
    template_name = 'app_catalog/catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Каталог'
        return context


class ProductDetailView(DetailView):
    """ Детальная страница товара. """
    template_name = 'app_catalog/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context['categories'] = self.object.categories.all()
        context['descr_points'] = self.object.descr_points.all()
        context['add_info_points'] = self.object.add_info_points.all()
        context['form'] = ReviewForm()
        context['reviews_count'] = 1
        return context

    def post(self, request, slug):
        form = ReviewForm(request.POST)
        if form.is_valid():
            return HttpResponse('Отзыв успешно добавлен.')
