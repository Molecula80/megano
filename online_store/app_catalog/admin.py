from django.contrib import admin
from .models import Category


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'parent', 'sort_index', 'active']
    list_filter = ['parent', 'sort_index', 'active']
    search_fields = ['title']
    inlines = [CategoryInline]
    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset):
        queryset.update(active=True)

    def mark_as_inactive(self, request, queryset):
        queryset.update(active=False)

    mark_as_active.short_description = 'Пометить как активные'
    mark_as_inactive.short_description = 'Пометить как неактивные'


admin.site.register(Category, CategoryAdmin)
