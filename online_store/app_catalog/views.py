from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.core.cache import cache
from django.db.models import Min
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

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
        popular_products = Product.objects.prefetch_related('categories').filter(active=True).order_by(
            '-sort_index')[:8]
        limited_edition = Product.objects.prefetch_related('categories').filter(
            active=True, limited_edition=True).order_by('-sort_index')[:16]
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
        context['sort_order'] = self.kwargs.get('sort_order')
        return context

    def get_queryset(self):
        """ Метод для вывода и фильтрации продуктов. """
        queryset = Product.objects.prefetch_related('categories').filter(active=True)
        form = ProductFilterForm(self.request.GET)
        if form.is_valid():
            queryset = self.filter_by_price(queryset=queryset, form=form)
            queryset = self.search_by_text(queryset=queryset, form=form)
            queryset = self.filter_by_choice_fields(queryset=queryset, form=form)
            queryset = self.filter_by_checkboxes(queryset=queryset, form=form)
        queryset = self.sort_products(queryset=queryset)
        return queryset

    @classmethod
    def filter_by_price(cls, queryset, form):
        """ Метод для фильтрации продуктов по цене. """
        # Рассчитываем минимальную и максимальную цены.
        price_range = form.cleaned_data.get('price_range').split(';')
        p_from = price_range[0]
        p_to = price_range[1]
        return queryset.filter(price__gte=p_from, price__lte=p_to)

    @classmethod
    def search_by_text(cls, queryset, form):
        """ Метод для поиска продуктов по нвзванию и описанию. """
        title = form.cleaned_data.get('title')
        if title:
            search_vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            search_query = SearchQuery(title)
            rank = SearchRank(search_vector, search_query)
            return queryset.annotate(search=search_vector, rank=rank).filter(search=search_query).order_by('-rank')
        return queryset

    @classmethod
    def filter_by_choice_fields(cls, queryset, form):
        """ Метод для поиска товаров по производителям и продавцам. """
        sellers = form.cleaned_data.get('sellers')
        if sellers:
            queryset = queryset.filter(seller__in=sellers)
        fabricators = form.cleaned_data.get('fabricators')
        if fabricators:
            queryset = queryset.filter(fabricator__in=fabricators)
        return queryset

    @classmethod
    def filter_by_checkboxes(cls, queryset, form):
        """ Метод для поиска товаров по чекбоксам. """
        in_stock = form.cleaned_data.get('in_stock')
        if in_stock is not None:
            queryset = queryset.filter(in_stock=in_stock)
        free_delivery = form.cleaned_data.get('free_delivery')
        if free_delivery is not None:
            queryset = queryset.filter(free_delivery=free_delivery)
        return queryset

    def sort_products(self, queryset):
        """ Сортирует товары. """
        # Возможные порядки сортировки.
        sort_orders = ['num_purchases', '-num_purchases', 'price', '-price', 'added_at', '-added_at']
        sort_order = self.kwargs.get('sort_order')
        if sort_order in sort_orders:
            return queryset.order_by(sort_order)
        return queryset


class ProductDetailView(DetailView):
    """ Детальная страница товара. """
    template_name = 'app_catalog/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs) -> dict:
        """ Метод для передачи параметров странице товара. """
        context = super().get_context_data(**kwargs)
        day = 60 * 60 * 24
        context['page_title'] = cache.get_or_set('page_title', self.object.title, day)
        context['categories'] = cache.get_or_set('categories', self.object.categories.all(), day)
        context['descr_points'] = cache.get_or_set('descr_points', self.object.descr_points.all(), day)
        context['add_info_points'] = cache.get_or_set('add_info_points', self.object.add_info_points.all(), day)
        # Если пользователь аутентифицирован, подставляем в форму его имя и email.
        context['form'] = ReviewForm(initial=self.get_initial_values(self.request.user))
        context['reviews'] = self.object.reviews.filter(active=True)
        context['reviews_count'] = cache.get_or_set('reviews_count', 0, day)
        return context

    def post(self, request, slug: str):
        """ Метод для добавления отзыва к товару. """
        # Если пользователь аутентифицирован, подставляем в форму его имя и email.
        form = ReviewForm(request.POST, initial=self.get_initial_values(request.user))
        if request.user.is_anonymous:
            form.add_error('__all__', 'Вам нужно авторизироваться, чтобы оставить отзыв.')
        if form.is_valid():
            review = form.save(commit=False)
            review.product = self.get_object()
            review.user = request.user
            review.save()
            return HttpResponseRedirect(reverse('app_catalog:product_detail', args=[slug]))
        return render(request, 'app_catalog/product_detail.html', context={
            'slug': slug,
            'page_title': self.get_object().title,
            'categories': self.get_object().categories.all(),
            'descr_points': self.get_object().descr_points.all(),
            'add_info_points': self.get_object().add_info_points.all(),
            'form': form,
            'reviews': self.get_object().reviews.filter(active=True),
            'reviews_count': 0,
        })

    @classmethod
    def get_initial_values(cls, user) -> dict:
        """ Возвращает словарь, содержащий имя и email пользователя, если последний аутентифицирован. """
        if user.is_authenticated:
            return {'name': user.full_name, 'email': user.email}
        return dict()
