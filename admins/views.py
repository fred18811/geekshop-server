from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from users.models import User
from products.models import Product
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProdactForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {
        'title': 'GeekShop - Admin',
    }
    return render(request, 'admins/index.html', context)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data()
        context['title'] = 'GeekShop - Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'GeekShop - Создание пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = 'GeekShop - Обновление\удаление пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


class ProdactListView(ListView):
    model = Product
    template_name = 'admins/admin-prodacts-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProdactListView, self).get_context_data()
        context['title'] = 'GeekShop - Продукты'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProdactListView, self).dispatch(request, *args, **kwargs)


class ProdactCreateView(CreateView):
    model = Product
    template_name = 'admins/admin-prodacts-create.html'
    form_class = ProdactForm
    success_url = reverse_lazy('admins:admin_prodacts')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProdactCreateView, self).get_context_data()
        context['title'] = 'GeekShop - Создание пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProdactCreateView, self).dispatch(request, *args, **kwargs)


class ProdactUpdateView(UpdateView):
    model = Product
    template_name = 'admins/admin-prodacts-update-delete.html'
    form_class = ProdactForm
    success_url = reverse_lazy('admins:admin_prodacts')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProdactUpdateView, self).get_context_data()
        context['title'] = 'GeekShop - Обновление\удаление товара'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProdactUpdateView, self).dispatch(request, *args, **kwargs)


class ProdactDeleteView(DeleteView):
    model = Product
    template_name = 'admins/admin-prodacts-update-delete.html'
    success_url = reverse_lazy('admins:admin_prodacts')

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProdactDeleteView, self).dispatch(request, *args, **kwargs)
