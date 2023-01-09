from django.contrib import admin
from .models import DeliveryMethod


class DeliveryMethodAdmin(admin.ModelAdmin):
    """ Административная модель способа доставки. """
    list_display = ['id', 'title', 'price', 'free_delivery_cost']


admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
