from .models import Category


def categories(request):
    return {'categories': Category.objects.filter(active=True).order_by('sort_index')}
