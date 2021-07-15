from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from users.models import User
from products.models import Product
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProdactForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {
        'title': 'GeekShop - Admin',
    }
    return render(request, 'admins/index.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
    context = {
        'title': 'GeekShop - Пользователи',
        'users': User.objects.all(),
    }
    return render(request, 'admins/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_staff)
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


@user_passes_test(lambda u: u.is_staff)
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
        'selected_user': selected_user
    }
    return render(request, 'admins/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_users_remove(request, pk):
    user = User.objects.get(id=pk)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admins:admin_users'))


@user_passes_test(lambda u: u.is_staff)
def admin_prodacts(request):
    context = {
        'title': 'GeekShop - Продукты',
        'prodacts': Product.objects.all(),
    }
    return render(request, 'admins/admin-prodacts-read.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_prodacts_create(request):
    if request.method == 'POST':
        form = ProdactForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_prodacts'))
    else:
        form = ProdactForm()
    context = {
        'title': 'GeekShop - Создание пользователя',
        'form': form,
    }
    return render(request, 'admins/admin-prodacts-create.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_prodacts_update(request, id):
    prodact = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProdactForm(instance=prodact, data=request.POST, files=request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_prodacts'))
    else:
        form = ProdactForm(instance=prodact)
    context = {
        'title': 'GeekShop - Обновление\удаление товара',
        'form': form,
        'prodact': prodact
    }
    return render(request, 'admins/admin-prodacts-update-delete.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_prodacts_remove(request, id):
    prodact = Product.objects.get(id=id)
    prodact.delete()
    return HttpResponseRedirect(reverse('admins:admin_prodacts'))