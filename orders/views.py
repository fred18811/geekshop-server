from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from products.models import Product
from baskets.models import Basket
from orders.forms import OrderItemForm
from orders.models import Order, OrderItem


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:order_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            formset = OrderFormset(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormset()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
            else:
                formset = OrderFormset()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        form.instance.user = self.request.user
        self.object = form.save()
        if orderitems.is_valid():
            orderitems.instance = self.object
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                basket_items.delete()
            orderitems.save()

        return super().form_valid(form)


class OrderItemUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:order_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.method == 'POST':
            data['orderitems'] = OrderFormset(self.request.POST, instance=self.object)
        else:
            formset = OrderFormset(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        form.instance.user = self.request.user
        self.object = form.save()
        if orderitems.is_valid():
            orderitems.instance = self.object
            orderitems.save()

        return super().form_valid(form)


class OrderItemsDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:order_list')


class OrderItemsRead(DetailView):
    model = Order


def order_forming_complete(request, pk):
    order_item = get_object_or_404(Order, pk=pk)
    order_item.status = Order.SENT_TO_PROCEED
    order_item.save()

    return HttpResponseRedirect(reverse('orders:order_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_on_server(sender, update_fields, instance, **kwargs):
    if instance.pk:
        if instance.product.quantity < instance.quantity - sender.objects.get(pk=instance.pk).quantity:
            instance.quantity = sender.objects.get(pk=instance.pk).quantity + instance.product.quantity
            instance.product.quantity -= instance.product.quantity
        elif instance.quantity < 0:
            instance.quantity = 0
            instance.product.quantity -= sender.objects.get(pk=instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity - sender.objects.get(pk=instance.pk).quantity
    else:
        if instance.product.quantity < instance.quantity:
            instance.quantity = instance.product.quantity
            instance.product.quantity -= instance.product.quantity
        elif instance.quantity < 0:
            instance.quantity = 1
            instance.product.quantity -= 1
        else:
            instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_on_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def product_price(request, pk):
    if request.is_ajax():
        product_item = Product.objects.filter(pk=pk).first()
        if product_item:
            return JsonResponse({'price': product_item.price})
        return JsonResponse({'price': 0})
