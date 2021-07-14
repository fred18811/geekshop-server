from django.shortcuts import render

def index(request):
    context = {
        'title': 'GeekShop - Admin',
    }
    return render(request, 'admins/index.html', context)

def admin_users(request):
    context = {
        'title': 'GeekShop - Пользователи',
    }
    return render(request, 'admins/admin-users-read.html', context)

def admin_users_create(request):
    context = {
        'title': 'GeekShop - Создание пользователя',
    }
    return render(request, 'admins/admin-users-create.html', context)

def admin_users_update_delete(request):
    context = {
        'title': 'GeekShop - Обновление\удаление пользователя',
    }
    return render(request, 'admins/admin-users-update_delete.html', context)