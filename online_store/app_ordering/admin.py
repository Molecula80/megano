from django.contrib import admin
from .models import Order, OrderItem, DeliveryMethod


class OrderItemInline(admin.TabularInline):
    """ Инлайн класс для редактирования пунктов описания товаров. """
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    """ Административная модель товара. """
    list_display = ['id', 'user', 'full_name', 'telephone', 'email', 'delivery_method', 'city', 'payment_method',
                    'delivery_price', 'total_cost', 'paid', 'created']
    list_filter = ['delivery_method', 'payment_method', 'paid']
    search_fields = ['id', 'full_name', 'email', 'city', 'address']
    inlines = [OrderItemInline]
    actions = ['mark_as_paid', 'mark_as_unpaid', 'mark_as_pending_payment']
    fieldsets = (
        ('Параметры пользователя', {
            'fields': ('user', 'full_name', 'telephone', 'email')
        }),
        ('Параметры доставки и оплаты', {
            'fields': ('delivery_method', 'city', 'address', 'payment_method', 'comment'),
            'classes': ['collapse']
        }),
        ('Статус заказа', {
            'fields': ('delivery_price', 'total_cost', 'paid', 'error_message'),
            'classes': ['collapse']
        })
    )

    def mark_as_paid(self, request, queryset) -> None:
        """ Помечает заказы как оплаченные. """
        queryset.update(paid=True)

    def mark_as_unpaid(self, request, queryset) -> None:
        """ Помечает заказы как не оплаченные. """
        queryset.update(paid=False)

    def mark_as_pending_payment(self, request, queryset):
        """ Помечает заказы как ожилающие оплаты. """
        queryset.update(paid=None)

    mark_as_paid.short_description = 'Пометить как оплаченные'
    mark_as_unpaid.short_description = 'Пометить как неоплаченные'
    mark_as_pending_payment.short_description = 'Пометить как ожидающие оплаты'


class OrderItemAdmin(admin.ModelAdmin):
    """ Административная модель единицы заказа. """
    list_display = ['id', 'order', 'product', 'price', 'quantity']


class DeliveryMethodAdmin(admin.ModelAdmin):
    """ Административная модель способа доставки. """
    list_display = ['id', 'title', 'price', 'free_delivery_cost']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
