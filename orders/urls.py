from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderList.as_view(), name='order_list'),
    path('read/<pk>', views.OrderList.as_view(), name='order_read'),
    path('update/<pk>', views.OrderList.as_view(), name='order_update'),
    path('delete/<pk>', views.OrderList.as_view(), name='order_delete'),
    path('create/', views.OrderItemCreate.as_view(), name='order_create'),
]