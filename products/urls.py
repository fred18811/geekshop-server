from django.urls import path
from products.views import ProdactsListView

app_name = 'products'

urlpatterns = [
    path('', ProdactsListView.as_view(), name='index'),
    path('page/<int:page>/', ProdactsListView.as_view(), name='page'),
    path('<int:category_id>/', ProdactsListView.as_view(), name='product'),
]
