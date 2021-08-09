from django.urls import path
from orders import views
from orders.views import order_forming_complete

app_name = 'orders'

urlpatterns = [
    path('', views.OrderList.as_view(), name='order_list'),
    path('read/<pk>', views.OrderItemsRead.as_view(), name='order_read'),
    path('update/<pk>', views.OrderItemUpdate.as_view(), name='order_update'),
    path('delete/<pk>', views.OrderItemsDelete.as_view(), name='order_delete'),
    path('create/', views.OrderItemCreate.as_view(), name='order_create'),
    path('complete/<pk>', order_forming_complete, name='order_forming_complete'),
]