from django.urls import path
from admins.views import index, admin_users_create, admin_users_update, admin_users, admin_users_remove, admin_prodacts, admin_prodacts_create, admin_prodacts_update, admin_prodacts_remove

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', admin_users, name='admin_users'),
    path('users/create', admin_users_create, name='admin_users_create'),
    path('users/update/<int:pk>', admin_users_update, name='admin_users_update'),
    path('users/remove/<int:pk>', admin_users_remove, name='admin_users_remove'),
    path('prodacts/', admin_prodacts, name='admin_prodacts'),
    path('prodacts/create', admin_prodacts_create, name='admin_prodacts_create'),
    path('prodacts/update/<int:id>', admin_prodacts_update, name='admin_prodacts_update'),
    path('prodacts/remove/<int:id>', admin_prodacts_remove, name='admin_prodacts_remove'),
]
