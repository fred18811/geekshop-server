from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm


def index(request):
    context = {
        'title': 'GeekShop - Admin',
    }
    return render(request, 'admins/index.html', context)


def admin_users(request):
    context = {
        'title': 'GeekShop - Пользователи',
        'users': User.objects.all(),
    }
    return render(request, 'admins/admin-users-read.html', context)


def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegistrationForm()
    context = {
        'title': 'GeekShop - Создание пользователя',
        'form': form,
    }
    return render(request, 'admins/admin-users-create.html', context)


def admin_users_update(request, pk):
    selected_user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = UserAdminProfileForm(instance=selected_user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminProfileForm(instance=selected_user)
    context = {
        'title': 'GeekShop - Обновление\удаление пользователя',
        'form': form,
        'selected_user':selected_user
    }
    return render(request, 'admins/admin-users-update-delete.html', context)

def admin_users_remove(request, pk):
    user = User.objects.get(id=pk)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admins:admin_users'))
