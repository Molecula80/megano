from .models import Category


def categories(request):
    return {'six_categories': Category.objects.filter(active=True).order_by('-sort_index')[:6]}
