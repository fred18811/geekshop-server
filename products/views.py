import datetime
import json

from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'GeekShop',
        'date' : datetime.datetime.now(),
    }
    with open('products/fixtures/goods.json', encoding='utf-8') as data_file:
        context['products'] = json.loads(data_file.read())
    return render(request, 'products/products.html', context)
