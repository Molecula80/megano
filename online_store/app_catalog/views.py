from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.core.cache import cache
from django.db.models import Min, Count, Q
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
        num_reviews = Count('reviews', filter=Q(reviews__active=True))  # Количество отзывов.
        products = Product.objects.annotate(num_reviews=num_reviews).prefetch_related('categories').\
            filter(active=True).order_by('-sort_index')
        popular_products = products[:8]
        limited_edition = products.filter(limited_edition=True)[:16]
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
        sort_orders = ['num_purchases', '-num_purchases', 'price', '-price', 'num_reviews', '-num_reviews', 'added_at',
                       '-added_at']
        sort_order = self.kwargs.get('sort_order')
        if sort_order in sort_orders:
            return queryset.order_by(sort_order)
        return queryset


def product_detail_view(request, slug):
    context = dict()
    product = get_object_or_404(Product, slug=slug)
    day = 60 * 60 * 24
    context['product'] = product
    context['page_title'] = cache.get_or_set('page_title', product.title, day)
    context['categories'] = cache.get_or_set('categories', product.categories.all(), day)
    context['descr_points'] = cache.get_or_set('descr_points', product.descr_points.all(), day)
    context['add_info_points'] = cache.get_or_set('add_info_points', product.add_info_points.all(), day)
    reviews = product.reviews.filter(active=True)
    context['reviews'] = reviews
    context['num_reviews'] = cache.get_or_set('num_reviews', reviews.count(), day)
    context['auth_error'] = False
    # Если пользователь аутентифицирован, подставляем в форму его имя и email.
    if request.user.is_authenticated:
        initial = {'name': request.user.full_name, 'email': request.user.email}
    else:
        initial = dict()
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
                review.save()
    else:
        form = ReviewForm(initial=initial)
    context['form'] = form
    return render(request, 'app_catalog/product_detail.html', context=context)

