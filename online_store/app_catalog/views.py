from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView
from django.core.cache import cache
from django.db.models import Min
from django_filters.views import FilterView

from .models import Category, Product
from .forms import ReviewForm, ProductFilterForm
from .filters import ProductFilter


class IndexView(TemplateView):
    """ Главная страница. """
    template_name = 'app_catalog/index.html'

    def get_context_data(self, **kwargs) -> dict:
        """ Метод для передачи параметров главной странице магазина. """
        context = super().get_context_data(**kwargs)
        tc_cache_key = 'three_categories'
        pp_cache_key = 'popular_products'
        le_cache_key = 'limited_edition'
        three_categories = Category.objects.filter(active=True).annotate(
            min_price=Min('products__price')).order_by('-sort_index')[:3]
        popular_products = Product.objects.prefetch_related('categories').filter(in_stock=True).order_by(
            '-sort_index')[:8]
        limited_edition = Product.objects.prefetch_related('categories').filter(
            in_stock=True, limited_edition=True).order_by('-sort_index')[:16]
        context['three_categories'] = cache.get_or_set(tc_cache_key, three_categories, 30)
        context['popular_products'] = cache.get_or_set(pp_cache_key, popular_products, 30)
        context['limited_edition'] = cache.get_or_set(le_cache_key, limited_edition, 30)
        return context


class ProductListView(FilterView):
    """ Страница со списком товаров. """
    template_name = 'app_catalog/catalog.html'
    context_object_name = 'products'
    paginate_by = 8
    filterset_class = ProductFilter

    def get_context_data(self, **kwargs) -> dict:
        """ Метод для данных страницы. """
        context = super().get_context_data(**kwargs)
        self.queryset = Product.objects.prefetch_related('categories').filter(active=True)
        context['page_title'] = 'Каталог'
        context['form'] = ProductFilterForm
        return context

    def post(self, request):
        """ Метод для применения фильтров. """
        form = ProductFilterForm(request.POST)
        if form.is_valid():
            price_range = form.cleaned_data.get('price_range').split(';')
            min_price = int(price_range[0])
            max_price = int(price_range[1])
            self.queryset = Product.objects.prefetch_related('categories').filter(active=True, price__gte=min_price,
                                                                                  price__lte=max_price)
        return render(request, 'app_catalog/catalog.html', context={'page_title': 'Каталог', 'form': form})


class ProductFilterView(ProductListView):
    """ Страница с отфильтрованным списком товаров. """
    def get_context_data(self, **kwargs) -> dict:
        """ Метод для данных страницы. """
        self.queryset = self.queryset.filter(price__gte=kwargs['min_price'], price__lte=kwargs['max_price'])
        context = super().get_context_data(**kwargs)
        return context


class ProductDetailView(DetailView):
    """ Детальная страница товара. """
    template_name = 'app_catalog/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs) -> dict:
        """ Метод для передачи параметров странице товара. """
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context['categories'] = self.object.categories.all()
        context['descr_points'] = self.object.descr_points.all()
        context['add_info_points'] = self.object.add_info_points.all()
        context['form'] = ReviewForm()
        context['reviews_count'] = 1
        return context

    def post(self, request, slug: str):
        """ Метод для добавления отзыва к товару. """
        form = ReviewForm(request.POST)
        if form.is_valid():
            return HttpResponse('Отзыв успешно добавлен.')
