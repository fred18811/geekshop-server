import datetime

from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'title':'GeekShop',
    }
    return render(request, 'products/index.html', context)

def products(request):
    context = {
        'title': 'GeekShop - Каталог',
        'products':[
            {'name':'Худи черного цвета с монограммами adidas Originals','price':6090,'description':'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.','img':'Adidas-hoodie.png'},
            {'name':'Синяя куртка The North Face','price':23725,'description':'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.','img':'Blue-jacket-The-North-Face.png'},
            {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN', 'price':3390, 'description': 'Материал с плюшевой текстурой. Удобный и мягкий.','img':'Brown-sports-oversized-top-ASOS-DESIGN.png'},
            {'name': 'Черный рюкзак Nike Heritage', 'price':2340, 'description': 'Плотная ткань. Легкий материал.','img':'Black-Nike-Heritage-backpack.png'},
            {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex', 'price':13590, 'description': 'гладкий кожаный верх. Натуральный материал.','img':'Black-Dr-Martens-shoes.png'},
            {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN', 'price':2890, 'description': 'легкая эластичная ткань сирсакер Фактурная ткань.','img':'Dark-blue-wide-leg-ASOs-DESIGN-trousers.png'},
        ],
        'date': datetime.datetime.now(),
    }
    return render(request, 'products/products.html', context)
