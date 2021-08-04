from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from orders.forms import OrderItemForm
from orders.models import Order, OrderItem


class OrderList(ListView):
    model = Order

    def get_querset(self):
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
            orderitems.save()

        return super().form_valid(form)