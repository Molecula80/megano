from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    """ Административная модель пользователя. """
    list_display = ['id', 'full_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['full_name', 'email']
    actions = ['mark_as_active', 'mark_as_inactive', 'assign_staff_status', 'deprive_staff_status',
               'assign_superuser_status', 'deprive_superuser_status']

    def mark_as_active(self, request, queryset) -> None:
        """ Помечает пользователей как активных. """
        queryset.update(is_active=True)

    def mark_as_inactive(self, request, queryset) -> None:
        """ Помечает пользователей как неактивных. """
        queryset.update(is_active=False)

    def assign_staff_status(self, request, queryset) -> None:
        """ Назначает пользователям статус персонала. """
        queryset.update(is_staff=True)

    def deprive_staff_status(self, request, queryset) -> None:
        """ Лишает пользователей статуса персонала. """
        queryset.update(is_staff=False)

    def assign_superuser_status(self, request, queryset) -> None:
        """ Назначает пользователям статус суперпользователя. """
        queryset.update(is_superuser=True)

    def deprive_superuser_status(self, request, queryset) -> None:
        """ Лишает пользователей статуса суперпользователя. """
        queryset.update(is_superuser=False)

    mark_as_active.short_description = 'Пометить как активные'
    mark_as_inactive.short_description = 'Пометить как неактивные'
    assign_staff_status.short_description = 'Назначить статус персонала'
    deprive_staff_status.short_description = 'Лишить статуса персонала'
    assign_superuser_status.short_description = 'Назначить статус суперпользователя'
    deprive_superuser_status.short_description = 'Лишить статуса суперпользователя'


admin.site.register(User, UserAdmin)
