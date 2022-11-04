# from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from django.core.cache import cache
from django.db.models import Min
from django.contrib.postgres.search import SearchVector

from .models import Category, Product
from .forms import ReviewForm, ProductFilterForm


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


class ProductListView(ListView):
    """ Страница со списком товаров. """
    template_name = 'app_catalog/catalog.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_context_data(self, **kwargs) -> dict:
        """ Метод для данных страницы. """
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Каталог'
        context['form'] = ProductFilterForm
        return context

    def get_queryset(self):
        """ Метод для вывода и фильтрации продуктов. """
        queryset = Product.objects.prefetch_related('categories').filter(active=True)
        form = ProductFilterForm(self.request.GET)
        if form.is_valid():
            queryset = self.filter_by_price(queryset=queryset, form=form)
            queryset = self.search_by_text(queryset=queryset, form=form)
        return queryset

    @classmethod
    def filter_by_price(cls, queryset, form):
        """ Метод для фильтрации продуктов по цене. """
        # Рассчитываем минимальную и максимальную цены.
        price_range = form.cleaned_data.get('price_range').split(';')
        p_from = price_range[0]
        p_to = price_range[1]
        return queryset.filter(price__gte=p_from, price__lte=p_to)

    def search_by_text(self, queryset, form):
        """ Метод для поиска продуктов по нвзванию и описанию. """
        if 'title' in self.request.GET:
            title = form.cleaned_data.get('title')
            return queryset.annotate(search=SearchVector('title', 'description')).filter(search=title)
        return queryset


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
