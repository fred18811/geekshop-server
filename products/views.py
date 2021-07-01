import datetime
import json

from django.shortcuts import render
from products.models import Product


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

    return render(request, 'products/products.html', context)
