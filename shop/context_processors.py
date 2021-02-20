from shop.models import Category
from django.core.cache import cache


def categories_list(request):
    categories = cache.get('categories_list')
    if not categories:
        categories = Category.objects.all()
        cache.set('categories_list', categories)
    return {'categories_list': categories}
