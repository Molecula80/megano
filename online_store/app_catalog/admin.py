from django.contrib import admin
from .models import Category, Fabricator, Product, DescrPoint, AddInfoPoint


class CategoryInline(admin.TabularInline):
    """ Инлайн класс для редактирования дочерних категорий товаров. """
    model = Category
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    """ Административная модель категории. """
    list_display = ['id', 'title', 'parent', 'sort_index', 'active']
    list_filter = ['parent', 'sort_index', 'active']
    search_fields = ['title']
    inlines = [CategoryInline]
    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset) -> None:
        """ Помечает категории как активные. """
        queryset.update(active=True)

    def mark_as_inactive(self, request, queryset) -> None:
        """ Помечает категории как неактивные. """
        queryset.update(active=False)

    mark_as_active.short_description = 'Пометить как активные'
    mark_as_inactive.short_description = 'Пометить как неактивные'


class ProductInline(admin.TabularInline):
    """ Инлайн класс для редактирования товаров. """
    model = Product
    extra = 0


class FabricatorAdmin(admin.ModelAdmin):
    """ Административная модель производителя. """
    list_display = ['id', 'title']
    search_fields = ['title']
    inlines = [ProductInline]


class DescrPointInline(admin.TabularInline):
    """ Инлайн класс для редактирования пунктов описания товаров. """
    model = DescrPoint
    extra = 0


class AddInfoPointInline(admin.TabularInline):
    """ Инлайн класс для редактирования пунктов дополнительной информации о товарах. """
    model = AddInfoPoint
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    """ Административная модель товара. """
    list_display = ['id', 'title', 'fabricator', 'price', 'num_purchases', 'sort_index', 'in_stock', 'free_delivery',
                    'limited_edition']
    list_filter = ['fabricator', 'sort_index', 'in_stock', 'free_delivery', 'limited_edition']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [DescrPointInline, AddInfoPointInline]
    actions = ['mark_as_in_stock', 'mark_as_out_of_stock', 'mark_as_free_delivery', 'mark_as_no_free_delivery',
               'mark_as_limited_edition', 'mark_as_unlimited_edition']
    fieldsets = (
        ('Основные сведения', {
            'fields': ('title', 'slug', 'description', 'price', 'image')
        }),
        ('Производитель и категории', {
            'fields': ('fabricator', 'categories'),
            'description': 'Сведения о производителе и категориях',
            'classes': ['collapse']
        }),
        ('Дополнительные сведения', {
            'fields': ('num_purchases', 'sort_index', 'added_at', 'in_stock', 'free_delivery', 'limited_edition'),
            'classes': ['collapse']
        })
    )

    def mark_as_in_stock(self, request, queryset) -> None:
        """ Помечает товары как имеющиеся в наличии. """
        queryset.update(in_stock=True)

    def mark_as_out_of_stock(self, request, queryset) -> None:
        """ Помечает товары как отсутствующие. """
        queryset.update(in_stock=False)

    def mark_as_free_delivery(self, request, queryset) -> None:
        """ Помечает товары как имеющие свободную доставку. """
        queryset.update(free_delivery=True)

    def mark_as_no_free_delivery(self, request, queryset) -> None:
        """ Помечает товары как не имеющие свободную доставку. """
        queryset.update(in_stock=False)

    def mark_as_limited_edition(self, request, queryset) -> None:
        """ Помечает как товары с ограниченным тиражом. """
        queryset.update(limited_edition=True)

    def mark_as_unlimited_edition(self, request, queryset) -> None:
        """ Помечает как товары с не ограниченным тиражом. """
        queryset.update(limited_edition=False)

    mark_as_in_stock.short_description = 'Пометить как имеющиеся в наличии'
    mark_as_out_of_stock.short_description = 'Пометить как отсутствующие'
    mark_as_free_delivery.short_description = 'Пометить как имеющие свободную доставку'
    mark_as_no_free_delivery.short_description = 'Пометить как не имеющие свободную доставку'
    mark_as_limited_edition.short_description = 'Пометить как ограниченный тираж'
    mark_as_unlimited_edition.short_description = 'Пометить как неограниченный тираж'


class DescrPointAdmin(admin.ModelAdmin):
    """ Административная панель пункта описания товара. """
    list_display = ['id', 'product', 'content']
    list_filter = ['product']
    search_fields = ['content']


class AddInfoPointAdmin(admin.ModelAdmin):
    """ Административная панель пункта дополнительной информации о товаре. """
    list_display = ['id', 'product', 'characteristic', 'value']
    list_filter = ['product']
    search_fields = ['characteristic', 'value']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Fabricator, FabricatorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(DescrPoint, DescrPointAdmin)
admin.site.register(AddInfoPoint, AddInfoPointAdmin)
