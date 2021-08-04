from django.shortcuts import render
from django.views.generic import ListView

from orders.models import Order


class OrderList(ListView):
    model = Order

    def get_querset(self):
        return Order.objects.filter(user=self.request.user)