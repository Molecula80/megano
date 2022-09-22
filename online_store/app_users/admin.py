from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'email', 'active']
    list_filter = ['active']
    search_fields = ['username', 'full_name', 'email']
    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset):
        queryset.update(active=True)

    def mark_as_inactive(self, request, queryset):
        queryset.update(active=False)

    mark_as_active.short_description = 'Пометить как активных'
    mark_as_inactive.short_description = 'Пометить как неактивных'


admin.site.register(User, UserAdmin)
