from django.db.models import F
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from users.models import User
from products.models import Product, ProductsCategory
from orders.models import Order
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProdactForm, OrderForm, ProdactCategoryForm
from django.db import connection


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {
        'title': 'GeekShop - Admin',
    }
    return render(request, 'admins/index.html', context)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


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


class OrderListView(ListView):
    model = Order
    template_name = 'admins/admin-orders-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data()
        context['title'] = 'GeekShop - Заказы'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(OrderListView, self).dispatch(request, *args, **kwargs)


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'admins/admin-orders-update.html'
    form_class = OrderForm
    success_url = reverse_lazy('admins:admin_orders')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderUpdateView, self).get_context_data()
        context['title'] = 'GeekShop - Обновление статуса заказа'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(OrderUpdateView, self).dispatch(request, *args, **kwargs)


class ProdactCategoryListView(ListView):
    model = ProductsCategory
    template_name = 'admins/admin-category-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProdactCategoryListView, self).get_context_data()
        context['title'] = 'GeekShop - Категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProdactCategoryListView, self).dispatch(request, *args, **kwargs)


class ProdactCategoryCreateView(CreateView):
    model = ProductsCategory
    template_name = 'admins/admin-category-create.html'
    form_class = ProdactCategoryForm
    success_url = reverse_lazy('admins:admin_categorys')

    def get_context_data(self, **kwargs):
        context = super(ProdactCategoryCreateView, self).get_context_data()
        context['title'] = 'GeekShop - Создание категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProdactCategoryCreateView, self).dispatch(request, *args, **kwargs)


class ProdactCategoryUpdateView(UpdateView):
    model = ProductsCategory
    template_name = 'admins/admin-category-update-delete.html'
    form_class = ProdactCategoryForm
    success_url = reverse_lazy('admins:admin_categorys')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProdactCategoryUpdateView, self).get_context_data()
        context['title'] = 'GeekShop - Обновление\удаление категории'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProdactCategoryUpdateView, self).dispatch(request, *args, **kwargs)


class ProdactCategoryDeleteView(DeleteView):
    model = ProductsCategory
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_categorys')

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProdactCategoryDeleteView, self).dispatch(request, *args, **kwargs)
