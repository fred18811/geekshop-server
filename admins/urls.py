from django.urls import path
from admins.views import index, admin_users_create, admin_users_update_delete, admin_users

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', admin_users, name='admin_users'),
    path('users/create', admin_users_create, name='admin_users_create'),
    path('users/update', admin_users_update_delete, name='admin_users_update_delete'),
]