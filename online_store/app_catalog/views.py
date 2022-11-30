import logging

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.core.cache import cache
from django.db.models import Min, Count, Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Category, Product
from .forms import ReviewForm, ProductFilterForm


logger = logging.getLogger(__name__)


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
        num_reviews = Count('reviews', filter=Q(reviews__active=True))  # Количество отзывов.
        products = Product.objects.annotate(num_reviews=num_reviews).prefetch_related('categories').\
            filter(active=True).order_by('-sort_index')
        popular_products = products[:8]
        limited_edition = products.filter(limited_edition=True)[:16]
        context['three_categories'] = cache.get_or_set(tc_cache_key, three_categories, 30)
        context['popular_products'] = cache.get_or_set(pp_cache_key, popular_products, 30)
        context['limited_edition'] = cache.get_or_set(le_cache_key, limited_edition, 30)
        logger.debug('Запрошена главная страница.')
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
        logger.debug('Запрошена страница со списком товаров.')
        return context

    def get_queryset(self):
        """ Метод для вывода и фильтрации продуктов. """
        num_reviews = Count('reviews', filter=Q(reviews__active=True))  # Количество отзывов.
        queryset = Product.objects.annotate(num_reviews=num_reviews).prefetch_related('categories').\
            filter(active=True).order_by('-sort_index')
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
        logger.debug('Выполнен поиск товаров стоимостью от {p_from} до {p_to} $.'.format(p_from=p_from, p_to=p_to))
        return queryset.filter(price__gte=p_from, price__lte=p_to)

    @classmethod
    def search_by_text(cls, queryset, form):
        """ Метод для поиска продуктов по нвзванию и описанию. """
        title = form.cleaned_data.get('title')
        if title:
            search_vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            search_query = SearchQuery(title)
            rank = SearchRank(search_vector, search_query)
            logger.debug('Выполнен поиск по строке {}.'.format(title))
            return queryset.annotate(search=search_vector, rank=rank).filter(search=search_query).order_by('-rank')
        return queryset

    @classmethod
    def filter_by_choice_fields(cls, queryset, form):
        """ Метод для поиска товаров по производителям и продавцам. """
        sellers = form.cleaned_data.get('sellers')
        if sellers:
            queryset = queryset.filter(seller__in=sellers)
            logger.debug('Выполнен поиск товаров от продавцов: {}'.format(sellers))
        fabricators = form.cleaned_data.get('fabricators')
        if fabricators:
            queryset = queryset.filter(fabricator__in=fabricators)
            logger.debug('Выполнен поиск товаров от производителей: {}'.format(fabricators))
        return queryset

    @classmethod
    def filter_by_checkboxes(cls, queryset, form):
        """ Метод для поиска товаров по чекбоксам. """
        in_stock = form.cleaned_data.get('in_stock')
        if in_stock is not None:
            queryset = queryset.filter(in_stock=in_stock)
            logger.debug('Выполнен поиск товаров с параметром "В наличии: {}"'.format(in_stock))
        free_delivery = form.cleaned_data.get('free_delivery')
        if free_delivery is not None:
            queryset = queryset.filter(free_delivery=free_delivery)
            logger.debug('Выполнен поиск товаров с параметром "Свободная доставка: {}"'.format(free_delivery))
        return queryset

    def sort_products(self, queryset):
        """ Сортирует товары. """
        # Возможные порядки сортировки.
        sort_orders = ['num_purchases', '-num_purchases', 'price', '-price', 'num_reviews', '-num_reviews', 'added_at',
                       '-added_at']
        sort_order = self.kwargs.get('sort_order')
        if sort_order in sort_orders:
            logger.debug('Товары отсортированы по параметру "{}"'.format(sort_order))
            return queryset.order_by(sort_order)
        return queryset


def product_detail_view(request, slug: str):
    """ Детальная страница товара. """
    context = dict()
    product = get_object_or_404(Product, slug=slug)
    logger.debug('Запрошена детальная страница товара "{}"'.format(product.title))
    day = 60 * 60 * 24
    context['product'] = product
    # Создаем уникальные ключи кеша для товара.
    context['page_title'] = cache.get_or_set('page_title{}'.format(product.id), product.title, day)
    context['categories'] = cache.get_or_set('categories{}'.format(product.id), product.categories.all(), day)
    context['descr_points'] = cache.get_or_set('descr_points{}'.format(product.id), product.descr_points.all(), day)
    context['add_info_points'] = cache.get_or_set('add_info_points{}'.format(product.id),
                                                  product.add_info_points.all(), day)
    reviews = product.reviews.filter(active=True).order_by('-added_at')
    context['num_reviews'] = cache.get_or_set('num_reviews{}'.format(product.id), reviews.count(), day)
    context['auth_error'] = False
    # Если пользователь аутентифицирован, подставляем в форму его имя и email.
    initial = get_initial_values(user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, initial=initial)
        if form.is_valid():
            # Если пользователь не аутентифицирован, выводим сообщение об ошибке.
            if request.user.is_anonymous:
                context['auth_error'] = True
            else:
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                logger.debug('Пользователь {email} оставил отзыв о товаре {product}'.format(
                    email=request.user.email,
                    product=product,
                ))
                review.save()
    else:
        form = ReviewForm(initial=initial)
    context['form'] = form
    return product_paginator(request=request, reviews=reviews, context=context)


def get_initial_values(user) -> dict:
    """ Возвращает словарь, содержащий имя и email пользователя, если последний аутентифицирован. """
    if user.is_authenticated:
        return {'name': user.full_name, 'email': user.email}
    return dict()


def product_paginator(request, reviews, context):
    """ Производит пагинацию отзывов к товару. """
    r_per_page = 3
    context['r_per_page'] = r_per_page
    paginator = Paginator(reviews, r_per_page)
    page = request.GET.get('page')
    context['num_pages'] = paginator.num_pages
    try:
        context['reviews'] = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую.
        context['reviews'] = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Если получили AJAX-запрос с номером страницы, большим, чем их количество, возвращаем пустую страницу.
            return HttpResponse('')
        # Если номер страницы больше, чем их количество, возвращаем последню.
        context['reviews'] = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'app_catalog/reviews_ajax.html', context=context)
    return render(request, 'app_catalog/product_detail.html', context=context)
