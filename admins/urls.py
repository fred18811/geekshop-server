from django.urls import path
from admins.views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView, ProdactListView, \
    ProdactCreateView, ProdactUpdateView, ProdactDeleteView, OrderListView, OrderUpdateView, ProdactCategoryListView,\
    ProdactCategoryDeleteView, ProdactCategoryUpdateView, ProdactCategoryCreateView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users/create', UserCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),
    path('users/remove/<int:pk>', UserDeleteView.as_view(), name='admin_users_remove'),
    path('prodacts/', ProdactListView.as_view(), name='admin_prodacts'),
    path('prodacts/create', ProdactCreateView.as_view(), name='admin_prodacts_create'),
    path('prodacts/update/<int:pk>', ProdactUpdateView.as_view(), name='admin_prodacts_update'),
    path('prodacts/remove/<int:pk>', ProdactDeleteView.as_view(), name='admin_prodacts_remove'),
    path('orders/', OrderListView.as_view(), name='admin_orders'),
    path('orders/update/<int:pk>', OrderUpdateView.as_view(), name='admin_order_update'),
    path('categorys/', ProdactCategoryListView.as_view(), name='admin_categorys'),
    path('category/create', ProdactCategoryCreateView.as_view(), name='admin_category_create'),
    path('category/update/<int:pk>', ProdactCategoryUpdateView.as_view(), name='admin_category_update'),
    path('category/remove/<int:pk>', ProdactCategoryDeleteView.as_view(), name='admin_category_remove'),
]