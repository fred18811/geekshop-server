import datetime

from django.shortcuts import render
from products.models import Product, ProductsCategory


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'GeekShop',
        'date': datetime.datetime.now(),
    }
    context['products'] = Product.objects.all()
    context['categorys'] = ProductsCategory.objects.all()

    return render(request, 'products/products.html', context)
