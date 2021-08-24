import datetime
from django.shortcuts import render
from products.models import Product, ProductsCategory
from django.views.generic.list import ListView
from django.conf import settings
from django.core.cache import cache


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def get_category_list():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductsCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductsCategory.objects.all()


class ProdactsListView(ListView):
    model = Product
    paginate_by = 3
    template_name = 'products/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProdactsListView, self).get_context_data()
        context['title'] = 'GeekShop - Каталог'
        context['date'] = datetime.datetime.now()
        context['categorys'] = get_category_list()
        return context

    def get_queryset(self):
        category_pk = self.request.GET.get('pk', None)
        qs = super().get_queryset()
        if category_pk:
            self.paginate_by = 0
            return qs.filter(category_id=category_pk)
        return qs
